#!/usr/bin/python
import threading
from furhatinterface import *

def Test(data):
    print("works")
    #print(data.text)


furhat = FurhatInterface("TestingFurhat", "192.168.43.131")
furhat.subscribe("furhatos.event.senses.SenseUsers", Test)

#furhat.subscribe("**", Test)
while True:
    input()
    furhat.changemode()