package furhatos.app.therapist

import furhatos.app.therapist.flow.*
import furhatos.app.therapist.logger.Logger
import furhatos.skills.Skill
import furhatos.flow.kotlin.*

var logHandler : Logger = Logger()
/*
    This is the entry point for the skill.
*/
class TherapistSkill : Skill() {
    override fun start() {
        logHandler.autoExport = true
        logHandler.startLogging()
        Flow().run(DialogInit)
    }
}

fun main(args: Array<String>) {
    Skill.main(args)
}
