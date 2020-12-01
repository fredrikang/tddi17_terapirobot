package furhatos.app.therapist.flow
import furhatos.app.therapist.nlu.CityEntity
import furhatos.app.therapist.nlu.MoodEntity
import furhatos.flow.kotlin.*
import furhatos.nlu.common.*


val AskNameState: State = state{
    include(goToControlledDialog)
    include(changeState)
    include(userEnterLeave)
    onEntry {
        targetUserName = furhat.askFor<PersonName>("Vad heter du?").toString()
        //targetUserName = name.toString()
        furhat.say("Hej $targetUserName, trevligt att träffas.")
        targetUserMood = furhat.askFor<MoodEntity>("Hur mår du i dag?").toString()
        //targetUserMood = mood.toString()
        val city = furhat.askFor<CityEntity>("I vilken stad bor du?")
        targetUserCity = city.toString()
        furhat.say("Okej, du bor i $targetUserCity")
    }


}