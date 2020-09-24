package furhatos.app.gettingstarted.flow

import furhatos.nlu.common.*
import furhatos.flow.kotlin.*

val MenuParent : State = state {
    include(menuButtons)
}

val Start : State = state(MenuParent) {
    
}

val menuButtons = partialState {
    onButton("Goto CameraFeed", id="0") 
    {
        goto(CameraFeedParent)
    }

    onButton("Tell Jens", id="1") 
    {
        furhat
    }
}

val cameraFeedButtons = partialState {
    onButton("Goto Start", id="0") 
    {
        goto(Start)
    }
    onButton("PORT", id="1") 
    {
        furhat.say(furhat.cameraFeed.port().toString())
        goto(Start)
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

val CameraFeedParent : State = state(MenuParent) {
    include(cameraFeedButtons)
} 