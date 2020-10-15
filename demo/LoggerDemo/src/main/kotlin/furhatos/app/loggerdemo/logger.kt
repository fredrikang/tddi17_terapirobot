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
 * Must have a client program running in the background of the "target client pc" for files to be exported.
 *
 * Should be a global variable, in for example "main.kt", as only one instance of the object should be used at a time.
 * Should be called in the corresponding "main.kt" file to get it started before any States are entered (this is not a requirement).
 * Should only be started ONCE per logging session, i.e. stop before starting a new one (unless maximum time is reached).
 */
package furhatos.app.loggerdemo
import furhatos.flow.kotlin.*
import java.io.File
import java.io.IOException
import java.net.ServerSocket
import java.net.Socket
import java.text.ParseException
import java.time.format.DateTimeFormatter
import kotlin.String as String

/**
 * Represents an event logger.
 * Can log communication and AI states.
 */
class Logger {
    var autoExport  : Boolean = false

    private var cloudTokenApi : String? = null
    private var sessionName   : String? = null
    private var logger        : DialogLogger = dialogLogger
    private var servSocket    : ServerSocket? = null


    /**
     * Default constructor.
     * Must use startLogging with all parameters for logging to function.
     * @return Logger object with all null values.
     */
    constructor()
    {
        servSocket = ServerSocket(8888) // Default port 8888
        servSocket!!.soTimeout = 5000        // Set 5s timeout for accepting clients.
    }

    /**
     * Constructor.
     * @param token Cloud token.
     * @return Logger object with set values based on parameters.
     */
    constructor (token: String?) {
        cloudTokenApi = token
        servSocket = ServerSocket(8888) // Default port 8888
        servSocket!!.soTimeout = 5000        // Set 5s timeout for accepting clients.
    }

    /**
     * Starts a logging session
     * If token is null no log will be uploaded to furhat cloud.
     * @param token Cloud token.
     */
    fun startLogging(token: String? = null) {
        sessionName = logger.timestamp("YYYY-MM-dd%YYHH-mm-ss") // Name based on AWS save format presented by furhat.io
        logger.startSession(name = null, cloudToken = token, maxLength = 3600)

        cloudTokenApi = token
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
     * Get the current year-month-day of this call.
     * @return Date as of the call to this function.
     */
    fun getDate(): String {
        return logger.timestamp("YYYY-MM-dd")
    }

    /**
     * Exports/Moves the most recent log from the furhat robot's memory.
     * Ends the current logging session!
     */
    private fun exportActiveLog() {
        logger.endSession()
        export()
    }

    /**
     * Clear logs from the robot's memory.
     * @param date Logs of this date will be deleted. If null all logs will be deleted.
     */
    fun clearLogsFromFurhatMem(date: String? = null) {
        try{
            for (log in File("/home/furnix/logs").listFiles {
                _,
                name
                -> when (date) {
                    null -> true
                    else -> name.contains(date)
                }
            }!!) {
                log.deleteRecursively()
            }
        } catch(e:IOException) {
            println("Failed to delete logs. ${e.message}\n${e.stackTrace}")
        }
    }

    /**
     * Exports/Moves log(s) from the robot memory to client.
     * @param arg Defines what way to export. "all" exports all files. If arg is a date ("YYYY-MM-dd") exports all logs from that day. null exports latest.
     * @param clear Removes read log(s) from robot memory if done.
     */
    fun export(arg : String? = null, clear : Boolean = false){
        if(arg != null){
            if(arg.toLowerCase() == "all") {
                exportAllLocalFiles(clear)
                return
            } else {
                try {
                    val formatter = DateTimeFormatter.ofPattern("YYYY-MM-dd"); formatter.format(formatter.parse(arg))
                    exportDateLogs(arg, clear)
                } catch(e:ParseException) {
                    println("Bad date format!")
                }
            }
        } else {
            exportLatestLog(clear)
        }
    }

    /**
     * Exports the latest modified log from the robot.
     */
    private fun exportLatestLog(clear : Boolean) {
        val logFile : File = findNewLogName() ?: return
        val session : String? = sessionName
        var socket  : Socket? = try { servSocket?.accept() } catch (e: IOException) { null }
        if (socket != null) {
            try {
                socket.getOutputStream()?.write(session!!.toByteArray())
                socket = servSocket?.accept() ?: return
                socket.getOutputStream()?.write(logFile.readBytes())
                if(clear) logFile.delete()
            } catch(e: IOException) {
                println("Failed to read file. " + e.message)
            }
        }
    }

    /**
     * Export all logs from the /logs/ folder that are of the specified date (YYYY-MM-DD).
     * If clear is set all read logs will be removed after they're exported.
     * @param date The date of the logs (YYYY-MM-DD)
     * @param clear Remove read files from robot after export.
     */
    private fun exportDateLogs(date : String, clear : Boolean = false){
        val folder = File("/home/furnix/logs")
        var socket : Socket?
        try{
            for(log in folder.listFiles{_, name -> name.contains(date)}!!) {
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
     * If clear is set all read logs will be removed after they're exported.
     * @param clear Remove all read files from robot after export.
     */
    private fun exportAllLocalFiles(clear : Boolean = false) {
        val folder = File("/home/furnix/logs")
        var socket : Socket?
        try{
            for(log in folder.listFiles()!!) {
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
     * @return Latest modified file.
     */
    private fun findNewLogName() : File? {
        val dir = File("/home/furnix/logs")
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
     * Stops the current logging session and exports all the logs to /user/FurhatLogs
     */
    fun stopLogging() {
        if(autoExport)
            exportActiveLog()
    }
}
