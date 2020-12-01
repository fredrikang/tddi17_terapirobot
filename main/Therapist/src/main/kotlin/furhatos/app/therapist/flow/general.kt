package furhatos.app.therapist.flow

import furhatos.event.Event
import furhatos.flow.kotlin.*

/*
    This partial state contains a standard response to users entering or leaving. This should be included in every
    state occurring during a session, if no specific other behaviour is desired. This state makes sure that
    the targetUser and hasTargetUser variables are correctly updated when users enter or leave.
*/
val userEnterLeave = partialState {
/*
        If the targetUser has been lost and a new user enters we once again check if the User is our patient.
        If the we are still focused on the target user we simply glance at the new user.
*/
    onUserEnter {
        if ( !users.hasTargetUser ) {
            furhat.attend(it)
            val resp = call(findTargetUser(it, "Är du min patient?", "Bra! Då fortsätter vi.", "Okej, jag förstår.")) as Boolean
            if (!resp) {
                furhat.attendNobody()
            }
        }
        else {
            furhat.glance(it)
        }
        reentry()
    }

/*
        If our target user leaves, variables concerning the target user are reset and furhat acknowledges audibly that the targetUser has been lost.
 */
    onUserLeave {
        if (it.id == users.targetUser) {
            users.hasTargetUser = false
            users.targetUser = "None"
            furhat.attendNobody()
            furhat.say("Huvudanvändare borta.")

        } else {
            furhat.say("Annan användare borta.") //Purely for debugging purposes.
        }
    }
}

/*
    This partial state is intended to provide a way to toggle between controlled dialog and the normal flow.
    Include this in partial states where such functionality is desired.
    reentry() is used to make sure that the most recent state entry function is repeated when returning.
*/
val goToControlledDialog = partialState {

    /*
        This trigger is used to enter into the controlled dialog state.
        The event is raised through the user interface, allowing the therapist to change mode at will.
    */
    onEvent("ChangeModeEvent") {
        send("CancelAutonomousState")
        call(controlledDialogState())
        reentry()
    }

    onEvent("CancelAutonomousState") {
        println("Exiting Autonomous State")
    }
}


val changeState = partialState {
/*
    onEvent<ChangeStateEvent> {
        furhat.say("Tog emot event.")
        when (it.stateName) {
            "DialogInit" -> goto(DialogInit)
            "Introduction" -> goto(Introduction)
            "SelectUser" -> goto(SelectUser)
            "AppearanceStateGender" -> goto(AppearanceStateGender)
            "Test" -> goto(Test)
            else -> {}
        }
  */


    onEvent("GoToDialogInitEvent") {
        goto(DialogInit)
    }
    onEvent("GoToIntroductionEvent") {
        goto(Introduction)
    }
    onEvent("GoToSelectUserEvent") {
        goto(SelectUser)
    }
    onEvent("GoToAppearanceStateGenderEvent") {
        goto(AppearanceStateGender)
    }
    onEvent("GoToTestEvent") {
        goto(Test)
    }

}

//class ChangeStateEvent(val stateName: String) : Event()
