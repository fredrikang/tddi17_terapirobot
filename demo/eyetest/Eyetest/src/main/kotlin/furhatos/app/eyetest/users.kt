package furhatos.app.eyetest.flow

import com.sun.org.apache.xpath.internal.operations.Bool
import furhatos.flow.kotlin.UserDataDelegate
import furhatos.flow.kotlin.NullSafeUserDataDelegate
import furhatos.records.Record
import furhatos.records.User
import furhatos.skills.UserManager


var User.disregard by NullSafeUserDataDelegate {false}

var hasTargetUserID : Boolean = false

var targetUserID : String = "None"

var UserManager.targetUser : String
    get() = targetUserID
    set(value) {targetUserID = value}

var UserManager.hasTargetUser : Boolean
    get() = hasTargetUserID
    set(value) { hasTargetUserID = value}