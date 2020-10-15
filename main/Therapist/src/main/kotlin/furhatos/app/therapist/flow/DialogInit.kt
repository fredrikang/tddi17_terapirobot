package furhatos.app.therapist.flow

import furhatos.autobehavior.userSpeechStartGesture
import furhatos.flow.kotlin.*
import furhatos.flow.kotlin.voice.Voice
import furhatos.util.*

/*
    This state is for initializing things that are necessary for the dialog flow.
*/
val DialogInit: State = state {
    init {
        //Set initial face texture and voice.
        furhat.voice = Voice(gender = Gender.FEMALE, language = Language.SWEDISH, pitch = "high")
        furhat.setInputLanguage(Language.SWEDISH)
        furhat.setTexture("Angelina")

        //disable smile on user speech
        furhat.userSpeechStartGesture = listOf()

        goto(Introduction)
    }
}

