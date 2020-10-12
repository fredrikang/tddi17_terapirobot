package furhatos.app.audiostreaming.flow

import furhatos.app.audiostreaming.flow.microphone.MicrophoneStreamingServer
import furhatos.flow.kotlin.State
import furhatos.flow.kotlin.furhat
import furhatos.flow.kotlin.onResponse
import furhatos.flow.kotlin.state
import furhatos.nlu.common.No
import furhatos.nlu.common.Yes
import furhatos.util.Gender
import furhatos.util.Language

val Start : State = state(Interaction) {

    onEntry {
        furhat.setVoice(Language.ENGLISH_US, Gender.MALE)

        furhat.say("Begin")

        try {
            val server = MicrophoneStreamingServer(8887)
            server.init()
            server.start()
        } catch (e: Exception) {
            furhat.say("Exception " + e.message)
            e.printStackTrace()
        }

        furhat.say("End")
    }

    onResponse<Yes>{
        furhat.say("I like humans.")
    }

    onResponse<No>{
        furhat.say("That's sad.")
    }
}
