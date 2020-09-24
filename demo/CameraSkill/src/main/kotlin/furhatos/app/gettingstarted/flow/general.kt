package furhatos.app.gettingstarted.flow

import furhatos.flow.kotlin.*
import furhatos.util.*

val Idle: State = state(MenuParent) {

    init {
        // Initialize the robot here
        furhat.setVoice(Language.ENGLISH_US, Gender.MALE)

        furhat.cameraFeed.enable()
        furhat.say(furhat.cameraFeed.port().toString())
        // End of initialization
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

val Interaction: State = state(MenuParent) {

    onUserLeave(instant = true) {
        if (users.count > 0) {
            if (it == users.current) {
                furhat.attend(users.other)
                goto(Start)
            } else {
                furhat.glance(it)
            }
        } else {
            goto(Idle)
        }
    }

    onUserEnter(instant = true) {
        furhat.glance(it)
    }

}

