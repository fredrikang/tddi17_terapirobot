package furhatos.app.eyetest

import furhatos.app.eyetest.flow.*
import furhatos.skills.Skill
import furhatos.flow.kotlin.*

class EyetestSkill : Skill() {
    override fun start() {
        Flow().run(Start)
    }
}

fun main(args: Array<String>) {
    Skill.main(args)
}
