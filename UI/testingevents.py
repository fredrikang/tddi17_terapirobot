#!/usr/bin/python
import threading
import os
import sys
import time
from furhatinterface import *
sys.path.insert(1, '/home/jesper/Documents/Programming/Skolarbete/tddi17_terapirobot/ExternalScripts/SpeechRecognition') 
from speechrecognition import SpeechRecognition

def Test(data):
    print("works")
    #print(data.text)


recognizer = SpeechRecognition(
        API_KEY_LOCATION=os.path.join('../ExternalScripts/_key', 'GAPI.json'), 
        save_audio_files=True
)

# Create thread for async recognition.
# Use thread for not stalling main thread and allow for better control.

furhat = FurhatInterface("TestingFurhat", "192.168.43.131")
#active_thread = threading.Thread(target=recognizer.recognize_async_audio_stream, args=( "sv-SE" , ) )       
#active_thread.start()
#furhat.subscribe("furhatos.event.senses.SenseUsers", Test)
#furhat.subscribe("**", Test)

recognizer.start_record_microphone()
time.sleep(5)
recognizer.stop_record_microphone()
furhat.speak(
    recognizer.recognize_sync_audio_file(
        file='./audio/' + recognizer.current_session[0] + '.raw',
        language_code="sv-SE"
    ))

#furhat.connectionstop()
#furhat.speak(recognizer.final_result_queue.get())
#while 1:
    #furhat.speak(input())
