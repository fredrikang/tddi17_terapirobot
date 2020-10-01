package furhatos.app.gettingstarted.flow

import furhatos.nlu.common.*
import furhatos.flow.kotlin.*


val greetingButtons = partialState {
    onButton("Goto Session", id="0") 
    {
        goto(Session)
    }

    onButton("Tell Jens", id="1") 
    {
        furhat.say("HELLO JENSIBOI")
    }
}

val sessionButtons = partialState {
    onButton("Goto Greeting", id="0") 
    {
        goto(Greeting)
    }
    onButton("PORT", id="1") 
    {
        furhat.say(furhat.cameraFeed.port().toString())
    }
    onButton("Is CameraFeedON", id="2") 
    {
        if(furhat.cameraFeed.isOpen())
            furhat.say("Yes, the camera feed is OPEN!")
        else
            furhat.say("No, the camera feed is CLOSED!")
    }
    onButton("Turn Camera feed on", id="3") 
    {
        furhat.cameraFeed.enable()
        if(furhat.cameraFeed.isOpen())
            furhat.say("Camera feed was turned on")
        else
            furhat.say("Unable to turn on camera feed")
    }
}