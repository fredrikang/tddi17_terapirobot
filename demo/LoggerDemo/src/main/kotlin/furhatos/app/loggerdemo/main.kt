
package furhatos.app.loggerdemo

import furhatos.app.loggerdemo.flow.*
import furhatos.skills.Skill
import furhatos.flow.kotlin.*
import kotlin.system.exitProcess

var logHandler : Logger = Logger()

class LoggerdemoSkill : Skill() {
    override fun start() {
        logHandler.export(arg=null, clear=false)
       // logHandler.clearLogsFromFurhatMem()
        exitProcess(1) // For debugging.
    }
}

fun main(args: Array<String>) {
    Skill.main(args)
}
