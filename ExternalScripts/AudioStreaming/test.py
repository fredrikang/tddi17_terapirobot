import pyaudio
import socket

p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                output=True)

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 8887         # The port used by the server

#with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
data = s.recv(1024)
while data != '':
	stream.write(data)
	data = s.recv(1024)

stream.stop_stream()
stream.close()

p.terminate()