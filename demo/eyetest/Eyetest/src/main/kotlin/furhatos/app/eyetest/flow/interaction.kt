package furhatos.app.eyetest.flow

import furhatos.app.eyetest.nlu.Nr1Intent
import furhatos.app.eyetest.nlu.Nr2Intent
import furhatos.nlu.common.*
import furhatos.flow.kotlin.*
import furhatos.gestures.Gestures
import furhatos.skills.SingleUserEngagementPolicy
import furhatos.nlu.common.Yes
import furhatos.nlu.common.No
import furhatos.records.User
import furhatos.skills.UserManager
import furhatos.util.Language
import furhatos.util.Gender
import furhatos.flow.kotlin.voice.Voice

val Start : State = state(Interaction) {
     init{
        //furhat.setVoice(Language.SWEDISH, Gender.FEMALE, true)
        furhat.voice = Voice(gender = Gender.FEMALE, language = Language.SWEDISH, pitch = "high")
        furhat.setInputLanguage(Language.SWEDISH)
        furhat.setTexture("Angelina")
     }

    /*  onEntry to make sure we ask all users in view of furhat if they are the intended patient.
        Users who have been establish to not be patients are marked with a diregard boolean. So that they can be ignored.
     */
    onEntry {
        if (users.count > 0) {
            for ( it in users.list){
                if (!it.disregard) {
                    furhat.attend(it)
                    val resp = call(findTargetUser(it, "Hej! Vill du prata med mig?", "Okej, trevligt att träffas!", "Okej, då pratar jag inte med dig.")) as Boolean
                    if (resp) {
                        goto(Appearance)
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
                goto(Appearance)
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


val Appearance : State = state(Interaction) {
    onEntry {
        furhat.say({+"Jag kan ta flera olika utseenden. Jag kan se ut så här."
                    +delay(2000)})
        furhat.voice = Voice(gender = Gender.FEMALE, language = Language.SWEDISH, pitch = "low")
        furhat.setInputLanguage(Language.SWEDISH)
        furhat.setTexture("Arianna")
        furhat.say("Jag kan också se ut så här.")
        furhat.ask("Vilket föredrar du, det första eller det andra?")
    }

    onResponse<Nr1Intent> {
        furhat.voice = Voice(gender = Gender.FEMALE, language = Language.SWEDISH, pitch = "high")
        furhat.setTexture("Angelina")
        goto(Test)
    }

    onResponse<Nr2Intent> {
        furhat.voice = Voice(gender = Gender.FEMALE, language = Language.SWEDISH, pitch = "low")
        furhat.setInputLanguage(Language.SWEDISH)
        goto(Test)
    }

    onExit {
        furhat.say("Okej, då tar jag det här utseendet.")
    }
}
val Test : State = state(Interaction) {
    onEntry {
        furhat.say("Gick in i teststadiet.")
        furhat.say("Den nuvarande användaren är.")
        furhat.say(users.targetUser) // For debugging purposes only.
    }

/*
        If the targetUser has been lost and a new user enters we once again check if the User is our patient.
        If the we are still focused on the target user we simply glance at the new user.
 */
    onUserEnter(instant = true) {
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
    }

/*
        If our target user leaves, variables concerning the target user are reset and furhat acknowledges audibly that the targetUser has been lost.
 */
    onUserLeave(instant = true) {
        if (it.id == users.targetUser ) {
            users.hasTargetUser = false
            users.targetUser = "None"
            furhat.attendNobody()
            furhat.say ( "Huvudanvändare borta." )

        }
        else {
            furhat.say("Annan användare borta.") //Purely for debugging purposes.
        }
    }
}