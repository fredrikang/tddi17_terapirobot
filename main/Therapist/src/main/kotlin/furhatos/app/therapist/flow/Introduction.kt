package furhatos.app.therapist.flow
import furhatos.flow.kotlin.*

val Introduction: State = state {
    init {
        goto(SelectUser)
    }
}

