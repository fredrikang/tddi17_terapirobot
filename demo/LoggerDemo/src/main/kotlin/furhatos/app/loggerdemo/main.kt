package furhatos.app.loggerdemo

import furhatos.app.loggerdemo.flow.*
import furhatos.skills.Skill
import furhatos.flow.kotlin.*

var logHandler : Logger = Logger()

class LoggerdemoSkill : Skill() {
    override fun start() {
        logHandler.startLogging(debug = false, token = "e2cecca6-d817-4679-9cb9-90bf70d856d2")
        Flow().run(Idle)
    }
}

fun main(args: Array<String>) {
    Skill.main(args)
}
