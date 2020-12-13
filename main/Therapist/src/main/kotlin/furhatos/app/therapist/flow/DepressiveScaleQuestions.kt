package furhatos.app.therapist.flow
import furhatos.app.therapist.nlu.*
import furhatos.flow.kotlin.State
import furhatos.flow.kotlin.state
import furhatos.flow.kotlin.*

/*
    This file contains a naive implementation of the depressive scale questions test.
    Please note that this implementation is only intended as a demonstration, and should not be used as-is.
    Further, it is recommended that a real implementation asks each question in a separate state, possibly using
    a called state with the question sent as parameter and the result as return value, to improve the stability of the system.
    Answers are also only saved within the state, so transferring resulting variables to a place they can be saved
    is also heavily recommended.
    This state and related functions has not been tested, and no functionality is guaranteed.
*/

val DepressiveScaleQuestionsState: State = state{
    include(goToControlledDialog)
    include(changeState)
    include(userEnterLeave)

    onEntry {
        var answers = IntArray(9)
        furhat.say("Jag kommer fråga ett antal frågor om hur du känner dig. Svara på frågorna med aldrig, vissa dagar, mer än hälften av dagarna, eller nästan alltid.")
        answers[0] = furhat.askFor<DepressiveScaleEntity>("Saknar du intresse för eller nöje av att göra saker?").toString().toInt()
        answers[1] = furhat.askFor<DepressiveScaleEntity>("Känner du dig nedstämd, deprimerad eller hopplös?").toString().toInt()
        answers[2] = furhat.askFor<DepressiveScaleEntity>("Har du problem att somna, eller sover du för mycket?").toString().toInt()
        answers[3] = furhat.askFor<DepressiveScaleEntity>("Känner du dig orkeslös eller trött?").toString().toInt()
        answers[4] = furhat.askFor<DepressiveScaleEntity>("Har du dålig aptit, eller överäter du?").toString().toInt()
        answers[5] = furhat.askFor<DepressiveScaleEntity>("Har du negativa tankar om dig själv, eller känner du att du har svikit dig själv eller dina nära?").toString().toInt()
        answers[6] = furhat.askFor<DepressiveScaleEntity>("Har du svårt att koncentrera dig på saker, som att läsa tidningen eller se på TV?").toString().toInt()
        answers[7] = furhat.askFor<DepressiveScaleEntity>("Rör du dig eller talar du så långsamt att andra kan ha uppmärksammat det, eller känner du dig rastlös?").toString().toInt()
        answers[8] = furhat.askFor<DepressiveScaleEntity>("Tänker du att det skulle vara bättre om du inte levde, eller om du skulle skada dig på något vis?").toString().toInt()
        var highAnswers = 0
        for (i in answers) {
            if (i > 1) {
                ++highAnswers
            }
        }
        if (((answers[0] > 1 || answers[1] > 1) && highAnswers >= 5) || ((answers[0] > 1 || answers[1] > 1) && highAnswers >= 4 && answers[8] != 0)) {
            furhat.say("Du visar symptom på allvarlig deppression.")
        }
        else if (((answers[0] > 1 || answers[1] > 1) && highAnswers >= 2) || ((answers[0] > 1 || answers[1] > 1) && highAnswers >= 1 && answers[8] != 0)) {
            furhat.say("Du visar deppressiva syptom.")
        }
    }
}


/*
    English version of above state
*/
/*
val DepressiveScaleQuestionsState: State = state{

    include(goToControlledDialog)
    include(changeState)
    include(userEnterLeave)

    onEntry {
        var answers = IntArray(9)
        furhat.say("I am going to ask you a set of questions regarding your wellbeing. Please answer with not at all, several days, more than half the days or nearly every day.")
        answers[0] = furhat.askFor<DepressiveScaleEntity>("Do you have little interest or pleasure in doing things?").toString().toInt()
        answers[1] = furhat.askFor<DepressiveScaleEntity>("Do you feel down, depressed or hopeless?").toString().toInt()
        answers[2] = furhat.askFor<DepressiveScaleEntity>("Do you have trouble falling or staying asleep, or are you leeping too much?").toString().toInt()
        answers[3] = furhat.askFor<DepressiveScaleEntity>("Are you feeling tired or having little energy?").toString().toInt()
        answers[4] = furhat.askFor<DepressiveScaleEntity>("Do you have poor appetite, or are you overeating?").toString().toInt()
        answers[5] = furhat.askFor<DepressiveScaleEntity>("Are you feeling bad about yourself, or feeling that you are a failure or have let yourself and your family down?").toString().toInt()
        answers[6] = furhat.askFor<DepressiveScaleEntity>("Do you have trouble concentrating on things, such as reading the newspaper or watching television?").toString().toInt()
        answers[7] = furhat.askFor<DepressiveScaleEntity>("Are you moving or speaking so slowly that other people could have noticed? Or the opposite, being so fidgety or restless that you have been moving around a lot more than usual?").toString().toInt()
        answers[8] = furhat.askFor<DepressiveScaleEntity>("Have you thought that you would be better off dead or of hurting yourself in some way?").toString().toInt()

        var highAnswers = 0
        for (i in answers) {
            if (i > 1) {
                ++highAnswers
            }
        }
        if (((answers[0] > 1 || answers[1] > 1) && highAnswers >= 5) || ((answers[0] > 1 || answers[1] > 1) && highAnswers >= 4 && answers[8] != 0)) {
            furhat.say("You are showing major depressive symptoms.")
        }
        else if (((answers[0] > 1 || answers[1] > 1) && highAnswers >= 2) || ((answers[0] > 1 || answers[1] > 1) && highAnswers >= 1 && answers[8] != 0)) {
             furhat.say("You are showing depressive symptoms.")
        }
    }
}
*/
