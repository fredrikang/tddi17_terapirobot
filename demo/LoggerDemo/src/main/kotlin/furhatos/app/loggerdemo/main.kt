
package furhatos.app.loggerdemo

import furhatos.app.loggerdemo.flow.*
import furhatos.skills.Skill
import furhatos.flow.kotlin.*
import kotlin.system.exitProcess

var logHandler : Logger = Logger()

class LoggerdemoSkill : Skill() {
    override fun start() {
        logHandler.export(arg="all", clear=false)
        exitProcess(1) // For debugging.
        Flow().run(Idle)
    }
}

fun main(args: Array<String>) {
    Skill.main(args)
}
