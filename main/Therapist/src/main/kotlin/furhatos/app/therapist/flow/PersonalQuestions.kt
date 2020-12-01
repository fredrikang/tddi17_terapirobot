package furhatos.app.therapist.flow
import furhatos.flow.kotlin.*
import furhatos.nlu.common.*


val AskNameState: State = State{
    include(goToControlledDialog)
    include(changeState)
    include(userEnterLeave)
    onEntry {
        var name = furhat.askFor<PersonName>("Vad heter du?")
        /* UserName = name.toString() */
        furhat.say("Hej $name trevligt att träffas.")
    }


}