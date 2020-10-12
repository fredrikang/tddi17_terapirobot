package furhatos.app.eyetest.nlu

import furhatos.nlu.Intent
import furhatos.util.Language

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