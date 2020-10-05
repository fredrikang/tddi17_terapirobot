package furhatos.app.audiostreaming.flow

import furhatos.flow.kotlin.State
import furhatos.flow.kotlin.furhat
import furhatos.flow.kotlin.onResponse
import furhatos.flow.kotlin.state
import furhatos.nlu.common.No
import furhatos.nlu.common.Yes
import furhatos.util.Gender
import furhatos.util.Language
import java.io.ByteArrayOutputStream
import java.util.*
import javax.sound.sampled.*


//import furhatos.app.audiostreaming.nlu.*

val Start : State = state(Interaction) {

    onEntry {
        //dialogLogger.startSession(cloudToken = "")
        //dialogLogger.startSession()

        furhat.setVoice(Language.ENGLISH_US, Gender.MALE)

        furhat.say("Begin")

        val mixers = AudioSystem.getMixerInfo()
        /*for (i in mixers.indices) {
            furhat.say("$i" + mixers[i].getName() + " --> " + mixers[i].getDescription())
            //System.out.println((i+1)+". " + mixers[i].getName() + " --> " + mixers[i].getDescription() );
            val sourceLines = AudioSystem.getMixer(mixers[i]).sourceLineInfo
            for (j in sourceLines.indices) {
                val lineInfo = sourceLines[j]
                if (lineInfo is DataLine.Info) {
                    val dataLineInfo = lineInfo as DataLine.Info
                    val collect = Arrays.stream(dataLineInfo.formats)
                            .map { d -> d.toString() }
                            .collect(Collectors.joining())
                    furhat.say("Source: " + collect);
                }
            }
            val targetLines = AudioSystem.getMixer(mixers[i]).targetLineInfo
            for (j in targetLines.indices) {
                val lineInfo = targetLines[j]
                if (lineInfo is DataLine.Info) {
                    val dataLineInfo = lineInfo as DataLine.Info
                    val collect = Arrays.stream(dataLineInfo.formats)
                            .map { d -> d.toString() }
                            .collect(Collectors.joining())
                    furhat.say("Target: " + collect);
                }
            }
        }*/

        val s = AudioStreamingServer(8887)
        s.start()
        furhat.say("Server started on port: " + s.port)

        //furhat.say("Test")
        val format = AudioFormat(16000.0f, 16, 1, true, true) // built-in mic & ReSpeaker
        //furhat.say("Created format")
        var microphone: TargetDataLine
        val speakers: SourceDataLine
        try {
            //furhat.say("In try-catch")
            microphone = AudioSystem.getTargetDataLine(format, mixers[0]); // built-in mic (robot)
            //microphone = AudioSystem.getTargetDataLine(format, mixers[7]); // ReSpeaker (robot)
            //microphone = AudioSystem.getTargetDataLine(format, mixers[3]); // ReSpeaker (local)
            furhat.say("Found microphone")
            val info = DataLine.Info(TargetDataLine::class.java, format)
            //furhat.say("Microphone info " + info.toString())
            //microphone = AudioSystem.getLine(info) as TargetDataLine
            microphone.open(format)
            furhat.say("Opened microphone")
            val out = ByteArrayOutputStream()
            var numBytesRead: Int
            val CHUNK_SIZE = 1024
            val data = ByteArray(microphone.bufferSize / 5)
            microphone.start()
            furhat.say("Started microphone")
            var bytesRead = 0
            val dataLineInfo = DataLine.Info(SourceDataLine::class.java, format)
            speakers = AudioSystem.getLine(dataLineInfo) as SourceDataLine
            speakers.open(format)
            furhat.say("Opened speakers")
            speakers.start()
            furhat.say("Started speakers")
            while (bytesRead < 10000000) {
                numBytesRead = microphone.read(data, 0, CHUNK_SIZE)
                bytesRead += numBytesRead
                // write the mic data to a stream for use later
                out.write(data, 0, numBytesRead)
                s.broadcast(data.copyOfRange(0, numBytesRead))
                println(Arrays.toString(data.copyOfRange(0, numBytesRead)))
                // write mic data to stream for immediate playback
                //speakers.write(data.copyOfRange(0, numBytesRead), 0, numBytesRead)
                //speakers.write(data, 0, numBytesRead)
            }
            speakers.drain()
            speakers.close()
            microphone.close()
        } catch (e: Exception) {
            furhat.say("Exception " + e.message)
            e.printStackTrace()
        }

        furhat.say("End")
    }

    onResponse<Yes>{
        furhat.say("I like humans.")
    }

    onResponse<No>{
        furhat.say("That's sad.")
    }
}
