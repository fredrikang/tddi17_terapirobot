package furhatos.app.eyetest.flow

import furhatos.flow.kotlin.UserDataDelegate
import furhatos.flow.kotlin.NullSafeUserDataDelegate
import furhatos.records.Record
import furhatos.records.User
import furhatos.skills.UserManager


var User.disregard by NullSafeUserDataDelegate {false}
