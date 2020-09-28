package furhatos.app.eyetest.flow

import furhatos.nlu.common.*
import furhatos.flow.kotlin.*
import furhatos.gestures.Gestures
import furhatos.skills.SingleUserEngagementPolicy
import furhatos.nlu.common.Yes
import furhatos.nlu.common.No
import furhatos.records.User
import furhatos.skills.UserManager


val Start : State = state(Interaction) {
    /* init{
        users.engagementPolicy = (SingleUserEngagementPolicy())
    } */
    onEntry {
        if (users.count > 0) {
            for ( it in users.list){
                if (!it.disregard) {
                    furhat.attend(it)
                    goto(queryUser(it))
                }
            }
        }
    }
    onUserEnter(instant = true) {
        if (!it.disregard){
            furhat.attend(it)
            goto(queryUser(it))

        }
    }
}



fun queryUser(user: User) = state(parent = Interaction) {
    onEntry {
            furhat.ask("Hello! Do you want to speak to me?")
    }
    onResponse<Yes> {
            furhat.say( "Okay nice to meet you!")
            furhat.gesture(Gestures.BigSmile)
            goto(Test)
    }

    onResponse<No> {
            furhat.say("Okay, I won't speak to you.")
            user.disregard = true
            goto(Start)
    }
}

val Test : State = state(Interaction) {
    onEntry {
        furhat.say("Entered Test state.")
        furhat.gesture((Gestures.CloseEyes))
    }
}