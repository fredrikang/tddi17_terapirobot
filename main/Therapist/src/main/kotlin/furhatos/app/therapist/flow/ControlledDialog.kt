package furhatos.app.therapist.flow

import furhatos.flow.kotlin.furhat
import furhatos.flow.kotlin.state

/*
    This state is intended to be used whenever the robot is to be controlled remotely. This state is called through the
    "goToControlledDialog" partial state, in general.kt. This state can be reached from any state which includes
    this partial state, so that the normal flow can be interrupted and resumed whenever desired.
*/
fun controlledDialogState() = state {
    onEntry {
        furhat.say("Gick in i teststadie för fri dialog.")
        terminate()
    }

    /*
    TODO
    Here, we want to implement a way to trigger a return to the normal flow.
    onEVENT {
    terminate()
    }
     */
}