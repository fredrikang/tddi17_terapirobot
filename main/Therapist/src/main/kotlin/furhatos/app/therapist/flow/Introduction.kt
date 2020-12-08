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


        goto(AskNameState)
    }
}

