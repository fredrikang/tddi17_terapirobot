package furhatos.app.therapist.flow

import furhatos.flow.kotlin.State
import furhatos.flow.kotlin.state
import furhatos.flow.kotlin.*
import furhatos.app.therapist.Constants
import furhatos.flow.kotlin.voice.Voice
import furhatos.autobehavior.userSpeechStartGesture
import furhatos.util.*

/*
    This state may be used to remove gathered user information and return to the initial SelectUser state
*/
val ResetState : State = state {
    onEntry {
        //Clear list of disregarded users
        for (it in users.list) {
            it.disregard = false
        }

        //Clear all gathered user information
        hasTargetUser = false
        targetUser = "None"
        userName = ""
        userCity = ""
        userMood = ""
        userWellbeing = -1

        //Reset initial face texture and voice.
        furhat.voice = Voice(gender = Gender.FEMALE, language = Language.SWEDISH, pitch = "high", rate = Constants.SPEECH_SPEED)
        furhat.setInputLanguage(Language.SWEDISH)
        furhat.setTexture("Angelina")
        furhat.userSpeechStartGesture = listOf()

        goto(SelectUser)

    }
}