package furhatos.app.eyetest.flow

import furhatos.flow.kotlin.*
import furhatos.util.*

val Idle: State = state {

    init {
        furhat.setVoice(Language.ENGLISH_US, Gender.MALE)
        if (users.count > 0) {
            furhat.attend(users.random)
            goto(Start)
        }
    }

    onEntry {
        furhat.attendNobody()
    }

    onUserEnter {
        furhat.attend(it)
        goto(Start)
    }
}
val Attending = state {
    onEntry {
        furhat.say("Hello there")
    }
    onUserLeave {
        furhat.say("Goodbye")
    }
}
val Interaction: State = state {

}