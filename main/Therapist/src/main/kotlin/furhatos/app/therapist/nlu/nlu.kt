package furhatos.app.therapist.nlu

import furhatos.nlu.Intent
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