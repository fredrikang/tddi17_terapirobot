package furhatos.app.therapist.flow

import furhatos.app.therapist.logHandler
import furhatos.flow.kotlin.State
import furhatos.flow.kotlin.furhat
import furhatos.flow.kotlin.state

/*
    This state is for debug purposes only. It represents an end state.
*/
val EndState : State = state {
    include(userEnterLeave)
    include(goToControlledDialog)
    include(changeState)
    onEntry {
        /*
        furhat.say("Slut på konversation.")
        furhat.say("Den nuvarande användaren är.")
        furhat.say(targetUser)
        */
        logHandler.stopLogging()
    }
}