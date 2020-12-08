package furhatos.app.therapist.gestures

import furhatos.gestures.defineGesture
import furhatos.gestures.BasicParams.*
import furhatos.gestures.Gesture
import kotlin.reflect.full.declaredMemberProperties

/*
    Add a button in gestures.txt in the UI with the same action as the custom gesture
    in this file to be able to trigger the gesture during the controlled dialog state,
    for example "Custom Smile:MySmile" for a custom gesture called MySmile.
 */
object CustomGestures {

    // Example custom gesture from https://docs.furhat.io/gestures/ but longer
    val LongSmile = defineGesture("LongSmile") {
        frame(0.32, 0.72) {
            SMILE_CLOSED to 0.5
        }
        frame(0.2, 0.72){
            BROW_UP_LEFT to 1.0
            BROW_UP_RIGHT to 1.0
        }
        frame(0.16, 0.72){
            BLINK_LEFT to 0.1
            BLINK_RIGHT to 0.1
        }
        reset(2.04)
    }

    /* Automatically finds the gestures declared above using reflection */
    fun getByName(name: String): Gesture? {
        val properties = CustomGestures::class.declaredMemberProperties

        for (property in properties) {
            val gesture = property.get(this) as Gesture;
            if (gesture.name == name) {
                return gesture
            }
        }

        return null
    }
}