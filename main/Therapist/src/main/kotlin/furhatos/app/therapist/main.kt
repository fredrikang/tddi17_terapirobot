package furhatos.app.therapist

import furhatos.app.therapist.flow.*
import furhatos.skills.Skill
import furhatos.flow.kotlin.*

class TherapistSkill : Skill() {
    override fun start() {
        Flow().run(Init)
    }
}

fun main(args: Array<String>) {
    Skill.main(args)
}
