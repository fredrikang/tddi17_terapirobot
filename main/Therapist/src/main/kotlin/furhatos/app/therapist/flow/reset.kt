package furhatos.app.therapist.flow

import furhatos.flow.kotlin.State
import furhatos.flow.kotlin.state
import furhatos.flow.kotlin.*

/*
    This state may be used to remove gathered user information and return to the initial SelectUser state
*/
val ResetState : State = state {
    onEntry {
        hasTargetUser = false
        targetUser = "None"
        for (it in users.list) {
            it.disregard = false
        }
        userName = ""
        userCity = ""
        userMood = ""
        userWellbeing = -1
        goto(SelectUser)
    }
}