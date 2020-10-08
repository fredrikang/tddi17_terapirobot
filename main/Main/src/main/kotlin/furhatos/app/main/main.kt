package furhatos.app.main

import furhatos.app.main.flow.*
import furhatos.skills.Skill
import furhatos.flow.kotlin.*

class MainSkill : Skill() {
    override fun start() {
        Flow().run(Idle)
    }
}

fun main(args: Array<String>) {
    Skill.main(args)
}
