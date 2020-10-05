package furhatos.app.audiostreaming

import furhatos.app.audiostreaming.flow.*
import furhatos.skills.Skill
import furhatos.flow.kotlin.*

class AudioStreamingSkill : Skill() {
    override fun start() {
        Flow().run(Start)
    }
}

fun main(args: Array<String>) {
    Skill.main(args)
}
