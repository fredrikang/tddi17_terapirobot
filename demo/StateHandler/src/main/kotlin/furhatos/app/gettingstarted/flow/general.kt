package furhatos.app.gettingstarted.flow

import furhatos.flow.kotlin.*
import furhatos.util.*

val SessionIncludes: State = state {

    include(sessionButtons)
}

val GreetingIncludes: State = state {

    include(greetingButtons)
}

val Greeting: State = state(GreetingIncludes) {

    init {
        // Initialize the robot here
        furhat.setVoice(Language.ENGLISH_US, Gender.MALE)

        furhat.say("Greeting state initialize")
    }

    onEntry {
        furhat.attendNobody()
    }

    onUserEnter {
        furhat.attend(it)
        furhat.say("Hello new user")
    }

    onUserLeave {
        furhat.say("GoodBye")
    }
}

val Session: State = state(SessionIncludes) {

    onUserLeave(instant = true) {
        furhat.say("Session User Leave")
    }

    onUserEnter(instant = true) {
        furhat.say("Session User Enter")
    }

}


