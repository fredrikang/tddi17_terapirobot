package furhatos.app.eyetest.flow

import furhatos.nlu.common.*
import furhatos.flow.kotlin.*
import furhatos.gestures.Gestures
import furhatos.skills.SingleUserEngagementPolicy
import furhatos.nlu.common.Yes
import furhatos.nlu.common.No
import furhatos.records.User
import furhatos.skills.UserManager


val Start : State = state(Interaction) {
    /* init{
        users.engagementPolicy = (SingleUserEngagementPolicy())
    } */

    /*  onEntry to make sure we ask all users in view of furhat if they are the intended patient.
        Users who have been establish to not be patients are marked with a diregard boolean. So that they can be ignored.
     */
    onEntry {
        if (users.count > 0) {
            for ( it in users.list){
                if (!it.disregard) {
                    furhat.attend(it)
                    val resp = call(findTargetUser(it, "Hello! Do you want to speak to me?", "Okay nice to meet you!", "Okay, I won't speak to you.")) as Boolean
                    if (resp) {
                        goto(Test)
                    }
                    else {
                        furhat.attendNobody() // If no user can be established as the parient furhat will ignore all users.
                    }
                }
            }
        }
    }
    //If a new user enters furhat will ask if they are the patient.
    onUserEnter(instant = true) {
        if (!it.disregard){
            furhat.attend(it)
            val resp = call(findTargetUser(it, "Hello! Do you want to speak to me?", "Okay nice to meet you!", "Okay, I won't speak to you.")) as Boolean
            if (resp) {
                goto(Test)
            }
            else {
                furhat.attendNobody()
            }
        }
    }
}


/*
    The function for asking users if they are the intended target.
    Takes a user, a string for furhat to ask and strings for furhat to respond to YES/NO answers with.
    If the user answers Yes then the user is set to targetUser in the usermanager, we also record that a targetUser has been established. And we return a true bool.
    If the user answers No, we set the disregard bool to true so that this user isn't asked again. A false bool is returned.
 */
fun findTargetUser(user: User, stringAsk: String, stringYes: String, stringNo: String) = state(parent = Interaction) {
    onEntry {
            furhat.ask(stringAsk)
    }
    onResponse<Yes> {

            furhat.say( stringYes)
            furhat.gesture(Gestures.BigSmile)
            users.targetUser = user.id
            users.hasTargetUser = true
            terminate(true)
    }

    onResponse<No> {
            furhat.say(stringNo)
            user.disregard = true
            terminate(false)
    }
}

val Test : State = state(Interaction) {
    onEntry {
        furhat.say("Entered Test state.")
        furhat.say("Current user is.")
        furhat.say(users.targetUser) // For debugging purposes only.
    }

/*
        If the targetUser has been lost and a new user enters we once again check if the User is our patient.
        If the we are still focused on the tartget user we simply glance at the new user.
 */
    onUserEnter(instant = true) {
        if ( !users.hasTargetUser ) {
            furhat.attend(it)
            val resp = call(findTargetUser(it, "Are you my patient?", "Great let's continue.", "Okay I understand.")) as Boolean
            if (!resp) {
                furhat.attendNobody()
            }
        }
        else {
            furhat.glance(it)
        }
    }

/*
        If our target user leaves, variables concerning the target user are reset and furhat acknowledges audibly that the targetUser has been lost.
 */
    onUserLeave(instant = true) {
        if (it.id == users.targetUser ) {
            users.hasTargetUser = false
            users.targetUser = "None"
            furhat.attendNobody()
            furhat.say ( "Lost target user." )

        }
        else {
            furhat.say("Other user left.") //Purely for debugging purposes.
        }
    }
}