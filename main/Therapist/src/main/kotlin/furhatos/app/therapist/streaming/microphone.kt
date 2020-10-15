package furhatos.app.therapist.streaming

import java.io.ByteArrayInputStream
import java.io.ByteArrayOutputStream
import java.io.Closeable
import javax.sound.sampled.*

class Microphone(private val dataLine: TargetDataLine, private val audioFormat: AudioFormat) : Closeable {

    companion object {
        // Try to use one of these audio formats when finding one that works for a microphone, from best to worst
        // swapBytes must be updated below if the sample size is changed (default: 16 bits - 2 bytes)
        private val AUDIO_FORMATS_TO_TRY = listOf(
                AudioFormat(48000f, 16, 1, true, false),
                AudioFormat(48000f, 16, 1, true, true),
                AudioFormat(44100f, 16, 1, true, false),
                AudioFormat(44100f, 16, 1, true, true),
                AudioFormat(22050f, 16, 1, true, false),
                AudioFormat(22050f, 16, 1, true, true),
                AudioFormat(16000f, 16, 1, true, false),
                AudioFormat(16000f, 16, 1, true, true),
                AudioFormat(11025f, 16, 1, true, false),
                AudioFormat(11025f, 16, 1, true, true),
                AudioFormat( 8000f, 16, 1, true, false),
                AudioFormat( 8000f, 16, 1, true, true)
        )

        fun findMicrophones(): List<Microphone> {
            val microphones = mutableListOf<Microphone>()

            for (mixerInfo in AudioSystem.getMixerInfo()) {
                val mixer = AudioSystem.getMixer(mixerInfo)

                for (possibleAudioFormat in AUDIO_FORMATS_TO_TRY) {
                    val lineInfo = DataLine.Info(TargetDataLine::class.java, possibleAudioFormat)

                    // Try another format if it isn't supported by the current mixer
                    if (!mixer.isLineSupported(lineInfo))
                        continue

                    try {
                        val line = mixer.getLine(lineInfo) as TargetDataLine
                        line.open(possibleAudioFormat)

                        microphones.add(Microphone(line, possibleAudioFormat))

                        println("[$mixerInfo] Selected audio format " +
                                "#${AUDIO_FORMATS_TO_TRY.indexOf(possibleAudioFormat)}: $possibleAudioFormat")

                        // Break out when a working audio format has been found for the mixer
                        break
                    } catch (e: LineUnavailableException) {
                        // The current mixer doesn't support the audio format even though it says it does
                    }
                }
            }

            return microphones
        }
    }

    fun start() {
        dataLine.start()
    }

    fun getWavHeader(): ByteArray {
        // AudioSystem.write can build a WAV header based on our audio format
        val outputStream = ByteArrayOutputStream()
        val dummyStream = AudioInputStream(ByteArrayInputStream(ByteArray(0)), audioFormat, 0)
        AudioSystem.write(dummyStream, AudioFileFormat.Type.WAVE, outputStream)
        return outputStream.toByteArray()
    }

    fun read(b: ByteArray, off: Int, len: Int): Int {
        val read = dataLine.read(b, off, len)

        // Audio players expect that the data will be little endian,
        // so convert it if the microphone data is being recorded as big endian
        if (audioFormat.isBigEndian) {
            swapEndianness(b, off, len)
        }

        return read
    }

    private fun swapEndianness(b: ByteArray, off: Int, len: Int) {
        for (x in off until off + len step 2) {
            val temp = b[x]
            b[x] = b[x + 1]
            b[x + 1] = temp
        }
    }

    override fun close() {
        dataLine.stop()
        dataLine.close()
    }
}