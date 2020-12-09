package furhatos.app.therapist.flow
import furhatos.app.therapist.nlu.*
import furhatos.flow.kotlin.*
import furhatos.nlu.common.*

/*
This file contains a number of states containing questions for furhat to ask the user.
These questions are intended primarily to demonstrate how such gathering of data can be performed, and also
show how WildcardIntents and EnumIntents may be created and used.
Please note that all of these questions could theoretically be placed within a single state. However, users entering and
leaving, as well as other interruptions, then require far more complex handling. It is recommended to keep states small,
so that external disruptions interrupt the dialog flow as little as possible.
*/

/*
    This state simply asks for the user's name. This uses the built-in PersonName entity, and as such will only accept
    names.
 */
val AskNameState: State = state{
    include(goToControlledDialog)
    include(changeState)
    include(userEnterLeave)
    onEntry {
        targetUserName = furhat.askFor<PersonName>("Vad heter du?").toString()
        furhat.say("Hej $targetUserName.")
        goto(AppearanceStateGender)
    }
}

/*
    This asks for the user's mood, and uses a WildcardIntent, which is not error checked. It also uses
    randomization to vary the speech pattern of the robot.
*/
val AskMoodState: State = state{
    include(goToControlledDialog)
    include(changeState)
    include(userEnterLeave)
    onEntry {
        targetUserMood = furhat.askFor<MoodEntity>({random {
                                                    +"Hur mår du i dag?"
                                                    +"Hur står det till?"
                                                    +"Hur har du det?"
                                                    +"Hur är det?"
                                                     }}).toString()
        goto(AskCityState)
    }
}

/*
    This state also uses a WildcardEntity, and showcases how follow-up questions can be asked to better interact
    with the user.
 */
val AskCityState: State = state{
    include(goToControlledDialog)
    include(changeState)
    include(userEnterLeave)
    onEntry {
        targetUserCity = furhat.askFor<CityEntity>("Var kommer du ifrån?").toString()
        val livedLong = furhat.askYN("Jaså. Har du bott där länge?")
        when(livedLong) {
            true -> furhat.say("Ja, $targetUserCity är ju fint.")
            false -> {
                val previousCity = furhat.askFor<CityEntity>("Okej, var bodde du innan?")
                furhat.say("Okej, så du flyttade till $targetUserCity från $previousCity. Hoppas att du trivs i $targetUserCity.")
            }
        }
        goto(AskWellbeingState)
    }
}

/*
    This state uses an EnumEntity to only allow user to respond with the numbers one to ten. The response can then be
    used in different ranges to provoke different responses. The userElaboration variable is not currently used, but
    shows how specific onResponse triggers may be used in askFor statements..
 */
val AskWellbeingState: State = state{
    include(goToControlledDialog)
    include(changeState)
    include(userEnterLeave)
    onEntry {
        targetUserWellbeing = furhat.askFor<ScaleEntity>("Hur skulle du bedöma ditt almänna välbefinnande på en skala ett till tio?").toString().toInt()
        val userElaboration : GeneralEntity?
        when (targetUserWellbeing) {
            in 1..4 -> {
                userElaboration = furhat.askFor("Okej, så du mår inte så bra i dag. Har det hänt något särskilt?") {
                    onResponse<No> {
                        furhat.say("Okej, bara dåligt i allmänhet, alltså.")
                        goto(EndState)
                    }
                }
                furhat.say("Okej. Tråkigt att höra.")
            }
            in 5..7 -> furhat.say("En ganska vanlig dag, alltså.")
            in 8..10 -> furhat.say("Skönt att höra att du mår bra!")
            else -> furhat.say("Ogiltigt")
        }
        goto(EndState)
    }
}




