#!/usr/bin/python
import socket
from furhatevent import *
import threading
import collections


class SubscriptionHandler:
    def __init__(self):
        self.values = collections.defaultdict(set)
    def register(self, event, callback):
        self.values[event].add(callback)
    def remove(self, event, callback):
        self.values[event].remove(callback)
    def trigger(self, event, **kwargs):
        for callback in self.values.get(event, []):
            callback(**kwargs)


class FurhatTCPConnection():
    """This handles the RAW TCP connection to the Furhat robot.
    It is used the FurhatInterface class and should not be used by something else."""
    def __init__(self, name : str, host :str):
        threading.Thread.__init__(self)
        self.name = name
        self.host = host
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(.1)
        self.listen_thread = threading.Thread(target = self.listen)
        self.listen = False
        self.subscriptions = SubscriptionHandler()
    def connect(self):
        """This is called to connect to the robot"""
        print("Connecting to host: ", self.host, " on port: ", 1932)
       # self.socket.connect((self.host, 1932))
        self.listen_thread.start()
        #self.socket.send("CONNECT broker ", self.name, "\n")
    def listen(self):
        while self.listen:
            try:
                message = self.socket.recv(4096)
                #Trigger events here
                print("RECEIVED: ", message)
            except socket.timeout:
                pass

    def stop(self):
        """Stop the listen thread and use join to make it wait until it is done."""
        self.listen = False
        self.listen_thread.join()



    def send_event(self, event : FurhatEvent):
        """Used to send a event to the robot."""
        #self.socket.send(bytes("EVENT ", event.event_name, " -1 " +  event.byte_count() + "\n"))
        #self.socket.send(bytes(event))
        print("EVENT ", event.event_name, " -1 " +  event.byte_count() + "\n")
        print(event)
#To be removed
    def recv(self):
        data = self.socket.recv(self.BUFFER_SIZE)
        print("Recv: ", data)
#To be removed

class FurhatInterface():
    """This will handle all the communtication with the Furhat robot."""
    def __init__(self, name : str, host : str):
        self.connection = FurhatTCPConnection(name, host)
        self.connection.connect()

    def subscribe(self, event :str, callback : callable):
        self.connection.subscriptions.register(event, callback)



    """Used to send a event to the robot."""
    def speak(self, text: str, monitorWords = True):
        self.connection.send_event(SpeechEvent(text, monitorWords))

    def gaze(self, x: int, y:int, z:int, mode : str = 2,  speed : str = 2):
        self.connection.send_event(GazeEvent(Location(x, y, z), mode, speed))


def Test(data):
    print(data.connection.host)

def Test2(data):
    print(data.connection.name)

furhat = FurhatInterface("TestingFurhat", "192.168.43.90")
furhat.subscribe("a", Test)
furhat.subscribe("a", Test2)

while 1:
    #furhat.gaze(5,6,7)
    #furhat.speak(input())
    furhat.connection.subscriptions.trigger(input(), data = furhat)
    
  
