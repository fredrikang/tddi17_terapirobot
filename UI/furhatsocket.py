import socket
import sys


from furhatevent import *




class FurhatTCPConnection():
    def __init__(self, name : str, host :str):
        self.name = name
        self.host = host
        self.BUFFER_SIZE = 1024
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      
    def connect(self):
        print("Connecting to host: ", self.host, " on port: ", 1932)
       # self.socket.connect((self.host, 1932))
        #self.socket.send("CONNECT broker ", self.name, "\n")
    
    def send_event(self, event : FurhatEvent):
        #self.socket.send(bytes("EVENT ", event.event_name, " -1 " +  event.byte_count() + "\n"))
        #self.socket.send(bytes(event))
        print("EVENT ", event.event_name, " -1 " +  event.byte_count() + "\n")
        print(event)

    def recv(self):
        data = self.socket.recv(self.BUFFER_SIZE)
        print("Recv: ", data)


class FurhatInterface():
    def __init__(self, name : str, host : str):
        self.connection = FurhatTCPConnection(name, host)
        self.connection.connect()
    
    def speak(self, text: str, monitorWords = True):
        self.connection.send_event(SpeechEvent(text, monitorWords))

    def gaze(self, x: int, y:int, z:int, mode : str = 2,  speed : str = 2):
        self.connection.send_event(GazeEvent(Location(x, y, z), mode, speed))



furhat = FurhatInterface("TestingFurhat", "192.168.43.90")
while 1:
    furhat.gaze(5,6,7)
    furhat.speak(input())
    
  
