package furhatos.app.therapist.flow

import furhatos.gestures.Gestures
import furhatos.records.User

import furhatos.flow.kotlin.*

val SelectUser : State = state {
    include(goToControlledDialog)
    include(changeState)
    /*  onEntry to make sure we ask all users in view of furhat if they are the intended patient.
        Users who have been establish to not be patients are marked with a diregard boolean. So that they can be ignored.
    */
    onEntry {
        if (users.count > 0) {
            for (it in users.list){
                if (!it.disregard) {
                    furhat.attend(it)
                    val resp = call(findTargetUser(it, "Hej! Vill du prata med mig?", "Okej, trevligt att träffas!", "Okej, då pratar jag inte med dig.")) as Boolean
                    if (resp) {
                        goto(AppearanceStateGender)
                    }
                    else {
                        furhat.attendNobody() // If no user can be established as the patient furhat will ignore all users.
                    }
                }
            }
        }
    }
    //If a new user enters furhat will ask if they are the patient.
    onUserEnter(instant = true) {
        if (!it.disregard){
            furhat.attend(it)
            val resp = call(findTargetUser(it, "Hej! Vill du prata med mig?", "Okej, trevligt att träffas!", "Okej, då pratar jag inte med dig.")) as Boolean
            if (resp) {
                goto(AppearanceStateGender)
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
fun findTargetUser(user: User, stringAsk: String, stringYes: String, stringNo: String) = state {
    onEntry {
        val ans = furhat.askYN(stringAsk)
        if (ans == true) {
            furhat.say(stringYes)
            furhat.gesture(Gestures.BigSmile)
            users.targetUser = user.id
            users.hasTargetUser = true
        }
        else if (ans == false){
            furhat.say(stringNo)
            user.disregard = true
        }
        else {
            reentry()
        }
        terminate(ans)
     }
}