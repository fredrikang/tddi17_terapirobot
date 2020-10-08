package furhatos.app.eyetest.flow

import com.sun.org.apache.xpath.internal.operations.Bool
import furhatos.flow.kotlin.UserDataDelegate
import furhatos.flow.kotlin.NullSafeUserDataDelegate
import furhatos.records.Record
import furhatos.records.User
import furhatos.skills.UserManager

/* Adds a boolean to the User class, this is used in the start state to mark users who have already been established to not be the intended patient.
Handy to use for filtering out users we have no interest in.
 */
var User.disregard by NullSafeUserDataDelegate {false}



//Variables that will be used in the UserManager but can not be placed inside the class. But can be set/get as if it were part of UserManager
var hasTargetUserID : Boolean = false  //Bool to check if a targetUser has been established.
var targetUserID : String = "None" //String for the user ID of the targetUser, to send the target user as parameter into function calls.

//Adding get/set for the new variables "in" UserManager.
var UserManager.targetUser : String
    get() = targetUserID
    set(value) {targetUserID = value}

var UserManager.hasTargetUser : Boolean
    get() = hasTargetUserID
    set(value) { hasTargetUserID = value}