package furhatos.app.therapist.flow


import furhatos.flow.kotlin.NullSafeUserDataDelegate
import furhatos.records.User

/* Adds a boolean to the User class, this is used in the start state to mark users who have already been established to not be the intended patient.
Handy to use for filtering out users we have no interest in.
 */
var User.disregard by NullSafeUserDataDelegate {false}

/*
Variables that are stored as information about the current target user. They are not extensions of the user class, as
there is currently no guarantee that user objects are stored when a user leaves.
*/
var hasTargetUserID : Boolean = false  //Bool to check if a targetUser has been established.
var targetUserID : String = "None" //String for the user ID of the targetUser, to send the target user as parameter into function calls.
var userName : String = ""
var userCity : String = ""
var userMood : String = ""

//Adding get/set for the new variables "in" UserManager.
var targetUser : String
    get() = targetUserID
    set(value) {targetUserID = value}

var hasTargetUser : Boolean
    get() = hasTargetUserID
    set(value) { hasTargetUserID = value}

var targetUserName : String
    get() = userName
    set(value) { userName = value}

var targetUserCity : String
    get() = userCity
    set(value) { userCity = value}

var targetUserMood : String
    get() = userMood
    set(value) { userMood = value}