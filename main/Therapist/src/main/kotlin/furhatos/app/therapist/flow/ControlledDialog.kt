package furhatos.app.therapist.flow

import furhatos.flow.kotlin.furhat
import furhatos.flow.kotlin.state

/*
    This state is intended to be used whenever the robot is to be controlled remotely. This state is called through the
    "goToControlledDialog" partial state, in general.kt. This state can be reached from any state which includes
    this partial state, so that the normal flow can be interrupted and resumed whenever desired.
*/
fun controlledDialogState() = state {
    include(customGesture)

    /*
        This event terminates the controlled dialog state, returning to the calling state.
        As such, normal flow is restarted from the point of departure.
        The event used is the same event that triggered the state in the first place.
    */
    onEvent("ChangeModeEvent") {
        send("CancelControlledDialogState")
    }

    onEvent("CancelControlledDialogState") {
        println("Exiting Controlled Dialog.")
        terminate()
    }
}