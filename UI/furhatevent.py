import json
import datetime
import socket

class FurhatIncomingEvent(object):
    event_name = ""
    def __init__(self, j):
        self.__dict__ = json.loads(j)

class Location(object):
    def __init__(self, x : int, y:int, z:int):
        self.x = x
        self.y = y
        self.z = z 

class FurhatEvent(object):
    """Calculate the sum of value1 and value2."""
    eventCount = 0
    def __init__(self, event_name : str):
        self.event_id = FurhatEvent.eventCount
        self.event_time = "2020-10-15 15:14:28:5085" #str(datetime.datetime.now())
        self.event_real_time =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")[:-2]
        self.event_name = event_name
        FurhatEvent.eventCount += 1
    
    def print_event(self):
        print("EVENT -1 {} {}\n".format(self.event_name, self.__byte_count()) + str(self))
    
    def send(self, sock : socket):
        sock.send(bytes("EVENT -1 {} {}\n".format(self.event_name, self.__byte_count()), 'utf-8'))
        sock.send(bytes(str(self), 'utf-8'))
    
    def __byte_count(self):
        return str(len(bytes(self.__str__(), 'ascii')))   
    def __str__(self):
        return json.dumps(self.__dict__, indent=4, default=lambda o: o.__dict__)
    def __bytes__(self):
        return bytes(str(self), 'utf-8')

class SpeechEvent(FurhatEvent):
    def __init__(self, text: str, monitorWords : bool):
        super().__init__("furhatos.event.actions.ActionSpeech")
        self.text = text
        self.monitorWords = monitorWords

class SpeechStopEvent(FurhatEvent):
    def __init__(self, action: str = ""):
        super().__init__("furhatos.event.actions.ActionSpeechStop")
        if action:
            self.action = action

class VoiceEvent(FurhatEvent):
    def __init__(self, name:str, lang:str, gender:str, agent:str):
        super().__init__("furhatos.event.actions.ActionConfigVoice")
        self.name = name
        self.lang = lang
        self.gender = gender
        self.agent = agent

class ListenEvent(FurhatEvent):
    def __init__(self, context: int, endSilTimeout:int, noSpeechTimeout:int, maxSpeechTimeout:int, nbest: int):
        super().__init__("furhatos.event.actions.ActionListen")
        self.context = context
        self.endSilTimeout = endSilTimeout
        self.noSpeechTimeout = noSpeechTimeout
        self.maxSpeechTimeout = maxSpeechTimeout
        self.nbest = nbest

class ListenStopEvent(FurhatEvent):
    def __init__(self, action : int):
        super().__init__("furhatos.event.actions.ActionListenStop")
        self.action = action

class GestureEvent(FurhatEvent):
    def __init__(self, name: str):
        super().__init__("furhatos.event.actions.ActionGesture")
        self.name = name

class GazeEvent(FurhatEvent):
    def __init__(self, location: Location, mode : str, speed : str):
        super().__init__("furhatos.event.actions.ActionGaze")
        self.location = location
        self.mode = mode
        self.speed = speed

class FaceTextureEvent(FurhatEvent):
    def __init__(self, texture: str):
        super().__init__("furhatos.event.actions.ActionConfigFace")
        self.texture = texture

class LEDSolidEvent(FurhatEvent):
    def __init__(self, text: str):
        super().__init__("furhatos.event.actions.ActionSetSolidLED")
        self.text = text
        self.monitorWords = True

class AttendEvent(FurhatEvent):
    def __init__(self, text: str):
        super().__init__("furhatos.event.actions.ActionAttend")
        self.text = text
        self.monitorWords = True

class SkillConnectEvent(FurhatEvent):
    def __init__(self, text: str):
        super().__init__("furhatos.event.actions.ActionSkillConnect")
        self.text = text
        self.monitorWords = True