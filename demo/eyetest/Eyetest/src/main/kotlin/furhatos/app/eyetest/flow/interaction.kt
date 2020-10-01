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
                    val resp = call(findTargetUser(it, "Hello! Do you want to speak to me?", "Okay nice to meet you!", "Okay, I won't speak to you.")) as Boolean
                    if (resp) {
                        goto(Test)
                    }
                    else {
                        furhat.attendNobody()
                    }
                }
            }
        }
    }
    onUserEnter(instant = true) {
        if (!it.disregard){
            furhat.attend(it)
            val resp = call(findTargetUser(it, "Hello! Do you want to speak to me?", "Okay nice to meet you!", "Okay, I won't speak to you.")) as Boolean
            if (resp) {
                goto(Test)
            }
            else {
                furhat.attendNobody()
            }
        }
    }
}



fun findTargetUser(user: User, stringAsk: String, stringYes: String, stringNo: String) = state(parent = Interaction) {
    onEntry {
            furhat.ask(stringAsk)
    }
    onResponse<Yes> {

            furhat.say( stringYes)
            furhat.gesture(Gestures.BigSmile)
            users.targetUser = user.id
            users.hasTargetUser = true
            terminate(true)
    }

    onResponse<No> {
            furhat.say(stringNo)
            user.disregard = true
            terminate(false)
    }
}

val Test : State = state(Interaction) {
    onEntry {
        furhat.say("Entered Test state.")
        furhat.say("Current user is.")
        furhat.say(users.targetUser)
    }
    onUserEnter(instant = true) {
        if ( !users.hasTargetUser ) {
            furhat.attend(it)
            val resp = call(findTargetUser(it, "Are you my patient?", "Great let's continue.", "Okay I understand.")) as Boolean
            if (!resp) {
                furhat.attendNobody()
            }
        }
        else {
            furhat.glance(it)
        }
    }
    onUserLeave(instant = true) {
        if (it.id == users.targetUser ) {
            users.hasTargetUser = false
            users.targetUser = "None"
            furhat.attendNobody()
            furhat.say ( "Lost target user." )

        }
        else {
            furhat.say("Other user left.")
        }
    }
}