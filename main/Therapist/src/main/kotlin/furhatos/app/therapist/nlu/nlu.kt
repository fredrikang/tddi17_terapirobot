package furhatos.app.therapist.nlu

import furhatos.nlu.Intent
import furhatos.nlu.WildcardEntity
import furhatos.util.Language


//Used when choosing if the therapist should be male or female, in AppearanceStateGender state
class MaleIntent : Intent() {
    override fun getExamples(lang: Language): List<String> {
        return listOf(
                "man",
                "kille",
                "manlig",
                "manligt"
        )
    }
}

//Used when choosing if the therapist should be male or female, in AppearanceStateGender state
class FemaleIntent : Intent() {
    override fun getExamples(lang: Language): List<String> {
        return listOf(
                "tjej",
                "kvinna",
                "kvinnlig",
                "kvinnligt"
        )
    }
}

//Used when choosing specific appearance, in AppearanceStateSpecific state
class Nr1Intent : Intent() {
    override fun getExamples(lang: Language): List<String> {
        return listOf(
                "nummer ett",
                "det första",
                "första",
                "ettan",
                "alternativ ett"
        )
    }
}

//Used when choosing specific appearance, in AppearanceStateSpecific state
class Nr2Intent : Intent() {
    override fun getExamples(lang: Language): List<String> {
        return listOf(
                "nummer två",
                "det andra",
                "andra",
                "tvåan",
                "alternativ två"
        )
    }
}
/*
    Used when transferring to controlled dialog, obscure phrasing since this is intended mostly as debug.
    Not currently in use.
*/
class EnableControlledDialogIntent : Intent() {
    override fun getExamples(lang: Language): List<String> {
        return listOf(
                "Testa distans"
        )
    }
}

/*
Below are wildcard entities for various information relating to the target user. Please note that due to the nature
of wildcards, these intents can not reasonably be error checked. As such, any input will register as a "city", for
example. It is recommended in further development that these are replaced or extended with EnumEntities
to make the program more stable.
 */
class CityEntity : WildcardEntity("city", AskCityIntent())
class AskCityIntent(): Intent() {

    var city : CityEntity? = null

    override fun getExamples(lang: Language): List<String> {
        return listOf(
            "Jag bor i @city.",
            "@city",
            "I @city"
        )
    }
}

class MoodEntity : WildcardEntity("mood", AskMoodIntent())
class AskMoodIntent(): Intent() {

    var mood : MoodEntity? = null

    override fun getExamples(lang: Language): List<String> {
        return listOf(
            "Jag mår @mood",
            "Jag känner mig @mood",
            "Jag är @mood",
            "@mood"
        )
    }
}

/*
class xEntity : WildcardEntity("x", AskxIntent())
class AskxIntent(): Intent() {

    var x : xEntity? = null

    override fun getExamples(lang: Language): List<String> {
        return listOf(

        )
    }
}
 */