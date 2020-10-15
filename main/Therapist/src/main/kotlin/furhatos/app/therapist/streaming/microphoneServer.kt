package furhatos.app.therapist.streaming

import java.net.ServerSocket
import java.net.Socket
import java.net.SocketException

class MicrophoneStreamingServer(port: Int) : ServerSocket(port) {

    companion object {
        private const val BUFFER_SIZE = 1024
    }

    private val clients = mutableListOf<Socket>()

    private lateinit var microphone: Microphone

    fun init() {
        val microphones = Microphone.findMicrophones()

        // Any optional USB-connected microphone will come last,
        // and if it isn't connected, the built-in microphone will be last
        microphone = microphones.last()
    }

    fun start() {
        val thread = Thread {
            while (true) {
                val client = accept()
                try {
                    onConnection(client)
                    clients.add(client)
                } catch (e: SocketException) {
                    // onConnection couldn't communicate with the client
                }
            }
        }
        thread.name = "Microphone Server"
        thread.start()

        // Now we can start listening
        microphone.start()

        val thread2 = Thread {
            val buffer = ByteArray(BUFFER_SIZE)
            microphone.use {
                while (true) {
                    // Read from microphone and broadcast the data to all clients
                    val read = microphone.read(buffer, 0, buffer.size)
                    broadcast(buffer, 0, read)
                }
            }
        }
        thread2.name = "Microphone Streamer"
        thread2.start()
    }

    private fun onConnection(client: Socket) {
        println("Connection from $client established, sending WAV header..")
        client.getOutputStream().write(microphone.getWavHeader())
    }

    private fun broadcast(b: ByteArray, off: Int, len: Int) {
        val iterator = clients.iterator()

        while (iterator.hasNext()) {
            val next = iterator.next()
            try {
                next.getOutputStream().write(b, off, len)
            } catch (e: SocketException) {
                // Client disconnected, remove from clients list
                iterator.remove()
            }
        }
    }
}