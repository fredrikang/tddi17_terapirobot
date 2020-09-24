package $packageName

import furhatos.flow.kotlin.*
import furhatos.nlu.common.*

val Init = state {
    onEntry {
        furhat.ask("Hello world. Do you like robots?")
    }

    onResponse<Yes>{
        furhat.say("I like humans.")
    }

}
