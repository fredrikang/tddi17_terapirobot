package furhatos.app.therapist.flow

import furhatos.app.therapist.Constants
import furhatos.flow.kotlin.*
import furhatos.flow.kotlin.voice.Voice
import furhatos.util.Gender
import furhatos.util.Language
import furhatos.app.therapist.nlu.*


/*
    This is the first state involved in choosing the apperarance of the robot therapist. In this state, the patient
    is asked if they prefer a male or female therapist. This information is then carried over to the next state,
    where appearance can be fine-tuned. This state uses the MaleIntent and FemaleIntent intents to evaluate user
    choices.
*/
val AppearanceStateGender : State = state {
    include(userEnterLeave)
    include(goToControlledDialog)
    include(changeState)
    onEntry {
        furhat.say{+"Jag kan ta flera olika utseenden. Jag kan se ut som en kvinna"
                   +delay(1000)}
        furhat.voice = Voice(gender = Gender.MALE, language = Language.ENGLISH_GB, rate = Constants.SPEECH_SPEED)
        furhat.setTexture("Geremy")
        furhat.setInputLanguage(Language.SWEDISH)
        furhat.ask("Eller så kan jag se ut som en man. Vilket föredrar du, manligt eller kvinnligt?")
    }

    onReentry{
        furhat.ask("Vilket föredrar du, manligt eller kvinnligt?")
    }
    onResponse<MaleIntent> {
        furhat.say("Okej, då tar jag manligt utseende.")
        furhat.voice = Voice(gender = Gender.MALE, language = Language.ENGLISH_GB, rate = Constants.SPEECH_SPEED)
        furhat.setTexture("Geremy")
        furhat.setInputLanguage(Language.SWEDISH)
        call(AppearanceStateSpecifics(false))
        furhat.say("Jag ser fram emot att få lära känna dig bättre.")
        goto(AskMoodState)
    }

    onResponse<FemaleIntent> {
        furhat.say("Okej, då tar jag kvinnligt utseende.")
        furhat.voice = Voice(gender = Gender.FEMALE, language = Language.SWEDISH, pitch = "high", rate = Constants.SPEECH_SPEED)
        furhat.setTexture("Angelina")
        call(AppearanceStateSpecifics(true))
        furhat.say("Jag ser fram emot att få lära känna dig bättre.")
        goto(AskMoodState)
    }
}

/*
    In this state, appearance selection is finalized. Here, the user is given two different options
    according to the therapist gender chosen in the previous state.
*/
fun AppearanceStateSpecifics(female : Boolean) : State = state {
    include(userEnterLeave)
    include(goToControlledDialog)
    onEntry {
        furhat.say{+"Jag kan se ut så här."
            +delay(1000)}
        if(female)
        {
            furhat.voice = Voice(gender = Gender.FEMALE, language = Language.SWEDISH, rate = Constants.SPEECH_SPEED)
            furhat.setTexture("Arianna")
        }
        else{
            furhat.voice = Voice(gender = Gender.MALE, language = Language.ENGLISH_GB, pitch = "low", rate = Constants.SPEECH_SPEED)
            furhat.setTexture("Max")
            furhat.setInputLanguage(Language.SWEDISH)
        }
        furhat.say("Jag kan också se ut så här.")
        furhat.ask("Vilket föredrar du, det första eller det andra?")
    }
    onReentry{
        furhat.ask("Vilket föredrar du, det första eller det andra?")
    }

    onResponse<Nr1Intent> {
        if(female)
        {
            furhat.voice = Voice(gender = Gender.FEMALE, language = Language.SWEDISH, pitch = "high", rate = Constants.SPEECH_SPEED)
            furhat.setTexture("Angelina")
        }
        else{
            furhat.voice = Voice(gender = Gender.MALE, language = Language.ENGLISH_GB, rate = Constants.SPEECH_SPEED)
            furhat.setTexture("Geremy")
            furhat.setInputLanguage(Language.SWEDISH)
        }
        furhat.say("Okej, då tar jag det här utseendet.")
        terminate()
    }

    onResponse<Nr2Intent> {
        furhat.say("Okej, då tar jag det här utseendet.")
        terminate()
    }
}





