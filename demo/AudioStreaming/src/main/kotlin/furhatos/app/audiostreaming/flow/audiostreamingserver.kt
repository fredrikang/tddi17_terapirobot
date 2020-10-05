package furhatos.app.audiostreaming.flow

import org.java_websocket.WebSocket
import org.java_websocket.handshake.ClientHandshake
import org.java_websocket.server.WebSocketServer
import java.net.InetSocketAddress
import java.nio.ByteBuffer

class AudioStreamingServer(port: Int) : WebSocketServer(InetSocketAddress(port)) {

    override fun onOpen(conn: WebSocket, handshake: ClientHandshake) {
        println(conn.remoteSocketAddress.address.hostAddress + " connected")
    }

    override fun onClose(conn: WebSocket, code: Int, reason: String, remote: Boolean) {
        println("$conn left")
    }

    override fun onMessage(conn: WebSocket, message: String) {
        println("$conn: $message")
    }

    override fun onMessage(conn: WebSocket, message: ByteBuffer) {
        println("$conn: $message")
    }

    override fun onError(conn: WebSocket, e: Exception) {
        e.printStackTrace()
    }

    override fun onStart() {
        println("Started audio streaming server")
        connectionLostTimeout = 200
    }
}