package furhatos.app.therapist.flow
import furhatos.flow.kotlin.*

/*
    This state will contain the robot's introduction, in which it will eventually introduce itself to the patient.
*/
val Introduction: State = state {
    onEntry {

        //First, run through introduction
        furhat.say("Tillfälligt introduktionsstadie.")

        //When introduction is done,go to primary user selection in SelectUser state
        goto(SelectUser)
    }
}
