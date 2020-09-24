package $packageName

import ${packageName}.flow.*
import furhatos.skills.Skill
import furhatos.flow.kotlin.*

class ${skillName}Skill : Skill() {
    override fun start() {
        Flow().run(Idle)
    }
}

fun main(args: Array<String>) {
    Skill.main(args)
}
