package furhatos.app.gettingstarted

import furhatos.nlu.common.*
import furhatos.flow.kotlin.*

class ProgramHandler {

    public val nextAvailableButtonIndex = 0;
    public val ProgramToIncludes = hashMapOf<State, List<State>>();
    public class ProgramHandler constructor() {
        
    }

    public fun includeAll(program: State, func: ()) {
        val includeList = ProgramToIncludes[program];
        for(i in 1 until includeList.size) {
            func(includeList[i]);
        }
    }

    public fun openProgram(program: State) {
        includeAll(program);
        goto(program);
    }
}