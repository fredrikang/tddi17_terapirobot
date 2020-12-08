package furhatos.app.therapist.flow
import furhatos.app.therapist.Constants
import furhatos.app.therapist.streaming.MicrophoneStreamingServer
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
        furhat.voice = Voice(gender = Gender.FEMALE, language = Language.SWEDISH, pitch = "high", rate = Constants.SPEECH_SPEED)
        furhat.setInputLanguage(Language.SWEDISH)
        furhat.setTexture("Angelina")
        //disable smile on user speech
        furhat.userSpeechStartGesture = listOf()

        //Start audio server
        try {
            val server = MicrophoneStreamingServer(8887)
            server.init()
            server.start()
        } catch (e: Exception) {
            e.printStackTrace()
        }

        //Start video feed
        furhat.cameraFeed.enable()

        goto(SelectUser)
    }
}

