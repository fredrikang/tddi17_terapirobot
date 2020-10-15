import socket
import sys
import select
import json
import binascii
import time

class SpeechEvent(object):
    def __init__(self, text: str):
        self.event_id = 0
        self.event_name = "furhatos.event.actions.ActionSpeech"
        self.event_time = "2020-10-15 15:14:28:5085"
        self.text = text
        self.monitorWords = True


class FurhatTCPConnection:
    def __init__(self, host):
        self.host = host
        self.BUFFER_SIZE = 1024
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      
    
    def connect(self):
        print("Connecting to host: ", self.host, " on port: ", 1932)
        self.socket.connect((self.host, 1932))
    
    def send(self, message):
        self.socket.send(bytes(message,"utf-8"))
        #print(message)

    def recv(self):
        data = self.socket.recv(self.BUFFER_SIZE)
        print("Recv: ", data)


#print(json_data)
furhat = FurhatTCPConnection("192.168.43.90")
furhat.connect()
time.sleep(.5)
furhat.send("CONNECT broker TCP_TEST\n")
time.sleep(.5)
#furhat.send("SUBSCRIBE **\n")
while 1:
 # furhat.recv()
  speech = SpeechEvent(input())
  json_data = json.dumps(speech.__dict__, separators=(',', ':'))
  furhat.send("EVENT furhatos.event.actions.ActionSpeech -1 " +  str(len(bytes(json_data, 'ascii'))) + "\n")
  furhat.send(json_data)
