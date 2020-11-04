#!/usr/bin/python
import socket
from furhatevent import *
import threading
import collections
import time


class SubscriptionHandler:
    def __init__(self):
        self.values = collections.defaultdict(set)
    def register(self, event, callback):
        self.values[event].add(callback)
    def remove(self, event, callback):
        self.values[event].remove(callback)
    def trigger(self, event : FurhatIncomingEvent):
        for callback in self.values.get(event.event_name, []):
            callback(event)


class FurhatTCPConnection():
    """This handles the RAW TCP connection to the Furhat robot.
    It is used the FurhatInterface class and should not be used by something else."""
    def __init__(self, name : str, host :str):
        threading.Thread.__init__(self)
        self.name = name
        self.host = host
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(.1)
        self.listen_thread = threading.Thread(target = self.__listen)
        self.listen = True
        self.subscriptions = SubscriptionHandler()
    def connect(self):
        """This is called to connect to the robot"""
        print("Connecting to host: {} on port: {}".format(self.host, 1932))
        self.socket.connect((self.host, 1932))
        self.listen_thread.start()
        self.socket.send(bytes("CONNECT broker " + self.name + "\n","utf-8"))
    def __listen(self):
        while self.listen:
            try:
                message = self.socket.recv(4096).decode('utf-8')
                #Trigger events here
                if "EVENT" not in message: 
                    continue
                message = self.socket.recv(4096).decode('utf-8')
                event = FurhatIncomingEvent(message)
                print("RECEIVED EVENT: ", event.event_name)
                self.subscriptions.trigger(event)
            except socket.timeout:
                pass

    def stop(self):
        """Stop the listen thread and use join to make it wait until it is done."""
        self.listen = False
        self.listen_thread.join()

    def send_event(self, event : FurhatEvent):
        """Used to send a event to the robot."""
        event.print_event()
        event.send(self.socket)


class FurhatInterface():
    """This will handle all the communtication with the Furhat robot."""
    def __init__(self, name : str, host : str):
        self.connection = FurhatTCPConnection(name, host)
        self.connection.connect()

    """Used to subscribe to an event that is sent from the robot."""
    def subscribe(self, event :str, callback : callable):
        self.connection.subscriptions.register(event, callback)

    """Used to make the robot speak."""
    def speak(self, text: str, monitorWords = True):
        self.connection.send_event(SpeechEvent(text, monitorWords))
    """Used to make the robot look at a point(x, y, z)"""
    def gaze(self, x: int, y:int, z:int, mode : str = 2,  speed : str = 2):
        self.connection.send_event(GazeEvent(Location(x, y, z), mode, speed))


def Test(data):
    print(data.text)


#furhat = FurhatInterface("TestingFurhat", "192.168.137.1")
#furhat.subscribe("furhatos.event.actions.ActionSpeech", Test)

#while 1:
    #furhat.gaze(i,0,10)
#    furhat.speak(input())
    #furhat.connection.subscriptions.trigger(input(), data = furhat)
    
  
