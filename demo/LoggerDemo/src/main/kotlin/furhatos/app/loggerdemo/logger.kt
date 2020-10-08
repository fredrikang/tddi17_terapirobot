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
    var filename              : String? = null
    var debugActive           : Boolean = false
    var autoExport            : Boolean = true
    var sessions              : ArrayList<String> = ArrayList()
    var cloudSave             : Boolean = false

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
    constructor() { }

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
        if (cloudTokenApi != null) {
            servSocket = ServerSocket(8888) // Default port 8888
            servSocket!!.soTimeout = 5000        // Set 5s timeout for accepting clients.
        }
        debugActive = debug
    }

    /**
     * Starts a logging session based on class members.
     */
    fun startLogging(){
        sessionName = logger.timestamp("YYYY-MM-dd%YYHH-mm-ss") // Name based on AWS save format presented by furhat.io
        logger.startSession(name = filename, cloudToken = cloudTokenApi, maxLength = 3600)
        sessions.add(sessionName!!)
    }

    /**
     * Starts a logging session based on class members
     * @param logName The name of the log.
     */
    fun startLogging(logName: String){
        filename = logName
        sessionName = logger.timestamp("YYYY-MM-dd%YYHH-mm-ss") // Name based on AWS save format presented by furhat.io
        logger.startSession(name = filename, cloudToken = cloudTokenApi, maxLength = 3600)
        sessions.add(sessionName!!)
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
        sessions.add(sessionName!!)

        cloudTokenApi = token
        if (cloudTokenApi != null) {
            servSocket = ServerSocket(8888) // Default port 8888
            servSocket!!.soTimeout = 5000        // Set 5s timeout for accepting clients.
        }

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
    fun getLogger() : DialogLogger { return logger }

    /**
     * Get the current logging session's ID.
     * @return Furhat cloudToken for cloud saving. (null if no token)
     */
    fun getCloudToken() : String? { return cloudTokenApi }

    /**
     * See if current logger is cloud based or locally based
     * @return true if cloud based else false.
     */
    fun isCloudBased() : Boolean { return cloudSave }

    /**
     * Currently not working
     * @TODO find if any workaround is possible
     */
    fun startDebugLog() {
        val debugDirectory : File = File(System.getProperty("user.dir") + File.separator + "debug")

        if (!debugDirectory.exists())
            debugDirectory.mkdir()

        val log = File("$debugDirectory" + "debug.json")
        //furhatos.flow.kotlin.flowLogger.start(log)
    }

    /**
     * Exports/Moves all the logs locally from /user/.furhat/logs to the destination /user/FurhatLogs (temp name.)
     * Ends the current logging session!
     */
    fun exportActiveLog() {
        if (cloudSave) {
            exportLogCloudBased()
        } else {
            exportLocalBased()
        }
        logger.endSession()
    }

    /**
     * Exports/Moves the log files from the furhat robots local storage by sending over network to client.
     * Sends the session id followed by the file byte data.
     */
    fun exportLocalBased(){
        var fname = sessionName!!.split('%')[0] + " " + sessionName!!.split('%')[1].substring(2)
        val logFile : File = findNewLogName("/home/furnix/logs")
                ?: return
        var session : String? = sessionName
        var socket  : Socket? = try { servSocket?.accept() } catch (e: IOException) { null }
        if (socket != null) {
            try {
                socket?.getOutputStream()?.write(session!!.toByteArray())
                socket = servSocket?.accept()
                socket?.getOutputStream()?.write(logFile.readBytes())
                sessions!!.remove(session)
            } catch(e: IOException) {
                println("Failed to read file.")
                // DebugLogger for logging here.
            }
        }
    }

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
     *
     * @TODO Might work with searching through folders on the robot. Check if folders are created.
     */
    fun exportLogCloudBased(id : String? = sessionName) {
        var session : String? = id
        var url = "http://log-viewer.furhat.io/getSkillLog/$cloudIDToken/$id"
        var socket: Socket? = try { servSocket?.accept() } catch (e: IOException) { null }
        if (socket != null) {
            thread(start = true) {
                try {
                    socket?.getOutputStream()?.write(url.toByteArray())
                    sessions!!.remove(session)
                } catch(e: IOException) {
                    // DebugLogger for logging here.
                }
                return@thread
            }
        }
    }

    /**
     * Export/Copy all logs from AWS cloud to connected client.
     */
    fun exportAllLogsCloudBased() {
        var socket: Socket? = try { servSocket?.accept() } catch (e: IOException) { null }
        if (socket != null) {
           thread(start = true) {
               sessions!!.forEach {
                   id -> try { socket?.getOutputStream()?.write("http://log-viewer.furhat.io/getSkillLog/$cloudIDToken/$id".toByteArray()) } catch(e: IOException) { return@thread }
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
