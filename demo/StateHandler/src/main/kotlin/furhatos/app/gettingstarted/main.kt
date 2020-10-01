package furhatos.app.gettingstarted

import furhatos.app.gettingstarted.flow.*
import furhatos.skills.Skill
import furhatos.flow.kotlin.*

class StateHandlerSkill : Skill() {
    override fun start() {
        Flow().run(Greeting)
    }
}

fun main(args: Array<String>) {
    Skill.main(args)
}

