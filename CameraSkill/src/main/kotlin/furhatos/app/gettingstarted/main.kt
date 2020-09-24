package furhatos.app.gettingstarted

import furhatos.app.gettingstarted.flow.*
import furhatos.skills.Skill
import furhatos.flow.kotlin.*

class GettingstartedSkill : Skill() {
    override fun start() {
        Flow().run(Idle)
    }
}

fun main(args: Array<String>) {
    Skill.main(args)
}
