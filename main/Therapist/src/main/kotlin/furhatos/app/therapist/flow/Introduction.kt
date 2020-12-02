package furhatos.app.therapist.flow
import furhatos.app.therapist.nlu.ScaleEntity
import furhatos.flow.kotlin.*
import furhatos.nlu.common.*

/*
    This state will contain the robot's introduction, in which it will eventually introduce itself to the patient.
*/
val Introduction: State = state {
    include(goToControlledDialog)
    include(changeState)
    onEntry {
        //First, run through introduction
        //furhat.say("Tillfälligt introduktionsstadie.")

        //When introduction is done,go to primary user selection in SelectUser state
        //goto(Teststate)
        goto(SelectUser)
    }
}

val Teststate: State = state {
    onEntry {
        val testInt = furhat.askFor<ScaleEntity>("test?").toString()
        furhat.say(testInt)
        reentry()
    }
}
