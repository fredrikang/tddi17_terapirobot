package furhatos.app.therapist.nlu

import furhatos.nlu.Intent
import furhatos.nlu.WildcardEntity
import furhatos.util.Language
import furhatos.nlu.EnumEntity


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

class ScaleEntity : EnumEntity(stemming=false) {
    override fun getEnum(lang: Language) : List<String> {
        return listOf("1:en,ett,1", "2:två,2", "3:tre,3", "4:fyra,4", "5:fem,5", "6:sex,6", "7:sju,7", "8:åtta,8", "9:nio,9", "10:tio,10")
    }

    /*
    This override is necessary since furhat wants to return the numbers 3 and 6 using letters, which will invalidate use
    in int contexts.
     */
    override fun toString(): String {
        val ret = toText()
        when (ret) {
            "tre" -> return "3"
            "sex" -> return "6"
            else -> return ret
        }
    }
}

/*
Below are wildcard entities for various information relating to the target user. Please note that due to the nature
of wildcards, these intents can not reasonably be error checked. As such, any input will register as a "city", for
example. It is recommended in further development that these are replaced or extended with EnumEntities
to make the program more stable.
 */

class GeneralEntity : WildcardEntity("x", AskGeneralIntent())
class AskGeneralIntent(): Intent() {

    var x : GeneralEntity? = null

    override fun getExamples(lang: Language): List<String> {
        return listOf(
            "@x"
        )
    }
}

class CityEntity : WildcardEntity("city", AskCityIntent())
class AskCityIntent(): Intent() {

    var city : CityEntity? = null

    override fun getExamples(lang: Language): List<String> {
        return listOf(
            "Jag bor i @city.",
            "@city",
            "I @city",
            "På @city"
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
    --This is a template for a WildcardEntity--
class xEntity : WildcardEntity("x", AskxIntent())
class AskxIntent(): Intent() {

    var x : xEntity? = null

    override fun getExamples(lang: Language): List<String> {
        return listOf(

        )
    }
}
 */