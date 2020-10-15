package furhatos.app.therapist.flow
import furhatos.flow.kotlin.*

/*
    This state will contain the robot's introduction, in which it will eventually introduce itself to the patient.
*/
val Introduction: State = state {
    onEntry {

        //First, attend present users and run through introduction
        furhat.attendAll()
        furhat.say("Tillfälligt introduktionsstadie.")

        //When introduction is done, stop attending and go to primary user selection in SelectUser state
        furhat.attendNobody()
        goto(SelectUser)
    }
}

