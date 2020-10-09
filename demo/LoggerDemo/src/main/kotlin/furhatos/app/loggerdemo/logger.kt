/*
 * The logger enables logging of communication between user and robot as well as the states of the robot.
 *
 * Enables logging and exporting of log files from either cloud or robot to client /user/FurhatLogs.
 * Currently only supports the "dialogLogger" as the intended debugLogger can only get called in States
 *
 * Uses the Furhat DialogLogger.
 * Can save a log of up to 3600s (= 1h) before a new one is created.
 * Can save a log with any filename. This will however impact the browser UI as that debug console will stop working
 * if the log name is different from the standard format which is a timestamp.
 *
 * If cloud save is active all files have to be exported before the skill terminates (i.e. the skill where Logger is defined).
 * Must have a client program running in the background of the "target client pc" for files to be exported.
 *
 * Should be a global variable, in for example "main.kt", as only one instance of the object should be used at a time.
 * Should be called in the corresponding "main.kt" file to get it started before any States are entered (this is not a requirement).
 * Should only be started ONCE per logging session, i.e. stop before starting a new one (unless maximum time is reached).
 * Should be stopped at the end of the skill. The current log will save either way but will NOT automatically export.
 */
package furhatos.app.loggerdemo
import furhatos.flow.kotlin.*
import java.io.File
import java.io.FilenameFilter
import java.io.IOException
import java.net.ServerSocket
import java.net.Socket
import kotlin.concurrent.thread
import kotlin.math.log
import kotlin.system.exitProcess
import kotlin.String as String

/**
 * Represents an event logger.
 * Can log communication and AI states.
 */
class Logger {
    var filename    : String? = null
    var debugActive : Boolean = false
    var autoExport  : Boolean = true
    var cloudSave   : Boolean = false

    private var cloudIDToken  : String = "62df5e87-7fea-427a-9dc1-179a38107269"
    private var cloudTokenApi : String? = null
    private var sessionName   : String? = null
    private var logger        : DialogLogger = dialogLogger
    private var servSocket    : ServerSocket? = null


    /**
     * Default constructor.
     * Must use startLogging with all parameters for logging to function.
     * @return Logger object with all null values.
     */
    constructor() {}

    /**
     * Constructor.
     * May use any startLogging(...) function to start logging.
     * @param fname Preffered file/log name.
     * @param token Cloud token.
     * @param debug !Currently unused!.
     * @return Logger object with set values based on parameters.
     */
    constructor (fname: String?, token: String?, debug: Boolean = false) {
        filename = fname
        cloudTokenApi = token
        servSocket = ServerSocket(8888) // Default port 8888
        servSocket!!.soTimeout = 5000        // Set 5s timeout for accepting clients.

        debugActive = debug
    }

    /**
     * Starts a logging session based on class members.
     */
    fun startLogging() {
        sessionName = logger.timestamp("YYYY-MM-dd%YYHH-mm-ss") // Name based on AWS save format presented by furhat.io
        logger.startSession(name = filename, cloudToken = cloudTokenApi, maxLength = 3600)
    }

    /**
     * Starts a logging session based on class members
     * @param logName The name of the log.
     */
    fun startLogging(logName: String) {
        filename = logName
        sessionName = logger.timestamp("YYYY-MM-dd%YYHH-mm-ss") // Name based on AWS save format presented by furhat.io
        logger.startSession(name = filename, cloudToken = cloudTokenApi, maxLength = 3600)
    }

    /**
     * Starts a logging session
     * Sets member values based on parameters.
     * @param logName Preferred filename. Standard is a timestamp. If set to other than null the web UI will fail to print information.
     * @param token Cloud token.
     * @param debug !Currently unused!.
     */
    fun startLogging(logName: String?, token: String?, debug: Boolean = false) {
        sessionName = logger.timestamp("YYYY-MM-dd%YYHH-mm-ss") // Name based on AWS save format presented by furhat.io
        logger.startSession(name = logName, cloudToken = token, maxLength = 3600)

        cloudTokenApi = token
        servSocket = ServerSocket(8888) // Default port 8888
        servSocket!!.soTimeout = 5000        // Set 5s timeout for accepting clients.

        filename = logName
        if (debug && !debugActive) {
            debugActive = true
            //startDebugLog()
        }
    }

    /**
     * Get the active logger object.
     * @return Furhat logger object used.
     */
    fun getLogger(): DialogLogger {
        return logger
    }

    /**
     * Get the current logging session's ID.
     * @return Furhat cloudToken for cloud saving. (null if no token)
     */
    fun getCloudToken(): String? {
        return cloudTokenApi
    }

    /**
     * See if current logger is cloud based or locally based
     * @return true if cloud based else false.
     */
    fun isCloudBased(): Boolean {
        return cloudSave
    }

    /**
     * Get the current year-month-day of this call.
     * @return Date as of the call to this function.
     */
    fun getDate(): String {
        return logger.timestamp("YYYY-MM-dd")
    }

    /**
     * Exports/Moves all the logs locally from /user/.furhat/logs to the destination /user/FurhatLogs (temp name.)
     * Ends the current logging session!
     */
    fun exportActiveLog() {
        logger.endSession()
        if (cloudSave) {
            exportLogCloudBased()
        } else {
            exportLocalBased()
        }
    }

    /**
     * Clear logs from the robot's memory.
     * @param date Logs of this date will be deleted. If null all logs will be deleted.
     */
    @Suppress("RECEIVER_NULLABILITY_MISMATCH_BASED_ON_JAVA_ANNOTATIONS")
    fun clearLogsFromFurhatMem(date: String? = null) {
        try{
            for (log in File("/home/furnix/logs").listFiles {
                _,
                name
                -> when (date) {
                    null -> true
                    else -> name.contains(date)
                }
            }) {
                log.deleteRecursively()
            }
        } catch(e:IOException) {
            println("Failed to delete logs. ${e.message}\n${e.stackTrace}")
        }
    }

    /**
     * Exports/Moves the log files from the furhat robots local storage by sending over network to client.
     * Sends the session id followed by the file byte data.
     */
    fun exportLocalBased(){
        val logFile : File = findNewLogName("/home/furnix/logs") ?: return
        var session : String? = sessionName
        var socket  : Socket? = try { servSocket?.accept() } catch (e: IOException) { null }
        if (socket != null) {
            try {
                socket.getOutputStream()?.write(session!!.toByteArray())
                socket = servSocket?.accept() ?: throw(IOException("Failed to bind socket."))
                socket.getOutputStream()?.write(logFile.readBytes())
            } catch(e: IOException) {
                println("Failed to read file. " + e.message)
                // DebugLogger for logging here.
            }
        }
    }

    /**
     * Export all logs from the /logs/ folder that are of the specified date (YYYY-MM-DD).
     * If clear is set all files will be removed after they're exported.
     * @param date The date of the logs (YYYY-MM-DD)
     * @param clear Clear all files after export.
     */
    fun exportDateLogs(date : String, clear : Boolean = false){
        val folder : File = File("/home/furnix/logs")
        var socket : Socket?
        try{
            for(log in folder.listFiles{_, name -> name.contains(date)}) {
                socket = servSocket?.accept() ?: return
                socket.getOutputStream()?.write(log.name.toByteArray())
                socket = servSocket?.accept() ?: return
                socket.getOutputStream()?.write(File(log.path + File.separator + "dialog.json").readBytes())
                if(clear) log.deleteRecursively()
            }
        } catch (e:IOException){
            println("Failed to export.")
        }
    }

    /**
     * Export all files from the /logs/ folder.
     * If clear is set all files will be removed after they're exported.
     * @param clear Clear all files after export.
     */
    fun exportAllLocalFiles(clear : Boolean = false) {
        val folder : File = File("/home/furnix/logs")
        var socket : Socket?
        try{
            for(log in folder.listFiles()) {
                socket = servSocket?.accept() ?: return
                socket.getOutputStream()?.write(log.name.toByteArray())
                socket = servSocket?.accept() ?: return
                socket.getOutputStream()?.write(File(log.path + File.separator + "dialog.json").readBytes())
                if(clear) log.deleteRecursively()
            }
        } catch (e:IOException){
            println("Failed to export.")
        }
    }

    /**
     * Find the most recently modified log file.
     * Used as the timestamp seems to not be accurate.
     * @param path Directory to search in.
     * @return Latest modified file.
     */
    private fun findNewLogName(path : String) : File? {
        val dir = File(path)
        val files = dir.listFiles(File::isDirectory)
        var lastModifiedTime : Long = Long.MIN_VALUE
        var latest : File? = null
        if(files != null){
            for(file in files){
                if(file.lastModified() > lastModifiedTime){
                    latest = file
                    lastModifiedTime = latest.lastModified()
                }
            }
        }
        latest = File(latest?.path + File.separator + "dialog.json")
        return latest
    }

    /**
     * UNRELIABLE FUNCTION! Timestamp is unreliable on robot, avoid using this hack.
     *
     * Export/Copy specific log in the AWS cloud.
     * Opens socket to send url of log to listening client.
     * This can either be saved for later or instantly fetched on that clients computer.
     *
     * Requires a client connecting to getting data. If no client is connected logs will be
     * saved onto cloud only. Currently there's no local functionality for fetching these files.
     *
     * Creates a new thread for accepting and sending data.
     *
     * @param id session ID to export (formatted as YYYY-MM-DD%YY-HH-mm-ss)
     */
    fun exportLogCloudBased(id : String? = sessionName) {
        var session : String? = id
        var url = "http://log-viewer.furhat.io/getSkillLog/$cloudIDToken/$id"
        var socket: Socket? = try { servSocket?.accept() } catch (e: IOException) { null }
        if (socket != null) {
            thread(start = true) {
                try {
                    socket.getOutputStream()?.write(url.toByteArray())
                } catch(e: IOException) {
                    println("Failed to send url to client. " + e.message)
                }
                return@thread
            }
        }
    }

    /**
     * Stops the current logging session and exports all the logs to /user/FurhatLogs
     */
    fun stopLogging() {
        if(autoExport)
            exportActiveLog()
    }
}
