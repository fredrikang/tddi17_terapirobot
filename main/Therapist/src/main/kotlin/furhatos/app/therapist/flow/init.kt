package furhatos.app.therapist.flow

import furhatos.flow.kotlin.*
import furhatos.flow.kotlin.voice.Voice
import furhatos.util.*

val Init: State = state {
    init {
        furhat.voice = Voice(gender = Gender.FEMALE, language = Language.SWEDISH, pitch = "high")
        furhat.setInputLanguage(Language.SWEDISH)
        furhat.setTexture("Angelina")
        goto(Introduction)
    }
}

