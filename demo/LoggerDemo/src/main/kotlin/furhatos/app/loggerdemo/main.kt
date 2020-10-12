
package furhatos.app.loggerdemo

import furhatos.app.loggerdemo.flow.*
import furhatos.skills.Skill
import furhatos.flow.kotlin.*

var logHandler : Logger = Logger(fname = null, token = "b18904cd-ae51-48d8-89a5-998c23f27da9", debug = false)

class LoggerdemoSkill : Skill() {
    override fun start() {
        logHandler.cloudSave = false
        //logHandler.startLogging(debug = false, token = "b18904cd-ae51-48d8-89a5-998c23f27da9") // token sparas externt?
        Flow().run(Idle)
    }
}

fun main(args: Array<String>) {
    Skill.main(args)
}
