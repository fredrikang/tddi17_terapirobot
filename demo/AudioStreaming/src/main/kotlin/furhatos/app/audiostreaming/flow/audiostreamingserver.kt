package furhatos.app.audiostreaming.flow

import java.net.ServerSocket
import java.net.Socket
import java.util.*

class AudioStreamingServer(port: Int) : ServerSocket(port) {

    val clients = Collections.synchronizedList(ArrayList<Socket>())

    fun start() {
        Thread({
            while (true) {
                val client = accept()
                clients.add(client)
            }
        }).start()
    }

    fun broadcast(bytes: ByteArray) {
        clients.forEach {
            it.getOutputStream().write(bytes)
        }
    }
}