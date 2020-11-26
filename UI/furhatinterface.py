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
                print(message)
                if "EVENT" not in message: 
                    continue
                message = message.split("\n")[1]#self.socket.recv(4096).decode('utf-8')              
                event = FurhatIncomingEvent(message)
                #print("RECEIVED EVENT: ", event.event_name)
                self.subscriptions.trigger(event)
            except (socket.timeout, IndexError):
                pass

    def stop(self):
        """Stop the listen thread and use join to make it wait until it is done."""
        self.listen = False
        self.listen_thread.join()

    def send_event(self, event : FurhatEvent):
        """Used to send a event to the robot."""
        event.print_event()
        event.send(self.socket)
        self.subscriptions.trigger(event)
    def subscribe(self, event : str):
        """Used to send subscribe to an event from the robot."""
        
        self.socket.send(bytes("SUBSCRIBE {} \n".format(event),"utf-8"))

class FurhatInterface():
    """This will handle all the communtication with the Furhat robot."""
    def __init__(self, name : str, host : str):
        self.connection = FurhatTCPConnection(name, host)
        self.connection.connect()
        self.subscriptions = []


    def subscribe(self, event :str, callback : callable):
        """Used to subscribe to an event that is sent from the robot."""
        if not event in self.subscriptions:
            self.subscriptions.append(event)
            self.connection.subscriptions.register(event, callback)
            print(' '.join(self.subscriptions))
            self.connection.subscribe(' '.join(self.subscriptions))


    def speak(self, text: str, monitorWords = True):
        """Used to make the robot speak."""
        self.connection.send_event(SpeechEvent(text, monitorWords))
    def gaze(self, x: int, y:int, z:int, mode : str = 2,  speed : str = 2):
        """Used to make the robot look at a point(x, y, z)"""
        self.connection.send_event(GazeEvent(Location(x, y, z), mode, speed))
    def led(self, red: int, green:int, blue:int):
        """Used to make the robot look at a point(x, y, z)"""
        self.connection.send_event(LEDSolidEvent(red, green, blue))
    def change_mode(self):
        """Used to send a Custom ChangeModeEvent to the robot"""
        self.connection.send_event(ChangeModeEvent())
    def start_skill(self, name : str):
        """Used to send a SendSkill event to the robot"""
        self.connection.send_event(SkillConnectEvent(name))
    def goto(self, state_name : str):
        """Used to send a SendSkill event to the robot"""
        self.connection.send_event(ChangeStateEvent(state_name))


        
    
    
  
