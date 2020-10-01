/*
 * The logger enables logging of communication and between user and robot as well as the robots states.
 *
 * Enables logging and exporting of log files from /user/.furhat to /user/FurhatLogs
 * Currently only supports the "dialogLogger" as the intended debugLogger can only get called in States
 *
 * Uses the Furhat DialogLogger.
 * Can save a log of up to 3600s (= 1h) before a new one is created.
 * Can save a log with any filename. This will however impact the browser UI as that debug console will stop working
 * if the log name is different from the standard format which is a timestamp.
 *
 * Should be called in the corresponding "general.kt" file to get it started before any States are entered (this is not a requirement).
 * Should only be started ONCE per logging session, i.e. stop before starting a new one (unless maximum time is reached).
 * Should be stopped at the end of the skill. The current log will save either way but will NOT automatically export to the target LOG folder.
 */
package furhatos.app.loggerdemo
import furhatos.flow.kotlin.*
import java.io.File
import java.io.IOException

/**
 * Represents an event logger.
 * Can log communication and AI states.
 */
class Logger {
    var filename : String? = null
    var debugActive : Boolean = false
    private var logger: DialogLogger = dialogLogger

    /**
     * Starts a logging session
     * @param logName Preferred log filename. Standard is a timestamp. If set to other than null the web UI will fail to print information.
     * @param debug If true a debug file will be created in ./debug/ (WIP)
     */
    fun startLogging(logName: String? = null, debug: Boolean = true) {
        logger.startSession(name = logName, maxLength = 3600)
        this@Logger.filename = logName
        if (debug && !this@Logger.debugActive) {
            this@Logger.debugActive = true
            //startDebugLog()
        }
    }

    /**
     * Currently not working
     * @TODO find if any workaround is possible
     */
    fun startDebugLog() {
        val debugDirectory : File = File(System.getProperty("user.dir") + File.separator + "debug")

        if(!debugDirectory.exists())
            debugDirectory.mkdir()

        val log = File("$debugDirectory" + "debug.json")
        //furhatos.flow.kotlin.flowLogger.start(log)
    }

    /**
     * Exports/Moves all the logs from /user/.furhat/logs to the destination /user/FurhatLogs (temp name.)
     * Ends the current logging session!
     * @TODO: Fix button for UI
     */
    fun exportLogs() {
        logger.endSession()
        val logDirectory : File = File(System.getProperty("user.home") + File.separator + ".furhat")
        val targetDirectory : File = File(System.getProperty("user.home") + File.separator + "FurhatLogs")

        if(logDirectory.exists()) {
            if (!targetDirectory.exists()) {
                targetDirectory.mkdir()
            }

            try {
                logDirectory.copyRecursively(targetDirectory, true)
                logDirectory.deleteRecursively()
            } catch (e:IOException) {
                println("Failed to move logs.")
                e.printStackTrace()
            }

        } else {
            println("Couldn't find log directory!")
        }
    }

    /**
     * Stops the current logging session and exports all the logs to /user/FurhatLogs
     */
    fun stopLogging() {
        logger.endSession()
        exportLogs()
    }
}