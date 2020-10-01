package furhatos.app.gettingstarted

import furhatos.nlu.common.*
import furhatos.flow.kotlin.*

class ProgramHandler {

    public val nextAvailableButtonIndex = 0;
    public val ProgramToIncludes = hashMapOf<State, ArrayList<State>>();
    public class ProgramHandler constructor() {
        
    }

    public fun includeAll(program: State) {
        for(v in ProgramToIncludes[program]) {
            program.include(v)
        }
    }

    public fun openProgram(program: State) {
        includeAll(program);
        goto(program);
    }
}