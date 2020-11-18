# Python implementation of Google Speech To Text
Implementation in python using PyAudio and google.cloud to record and recognize speech.

The file ```UI/testingstt.py``` has the test for running with furhat.
Below is the ```testingstt.py``` example for running both streaming and recording.

```
import threading
import os
import time
from furhatinterface import *
from speechrecognition import SpeechRecognition


humanoids="10.137.31.224"
furhat = FurhatInterface("TestingFurhat", "192.168.43.131")

###
# Setup recognizer by setting the path to the Google API key .json file,
# and if the audio will be saved after exit of program or not.
#
# Note that if 'save_audio_files=False' the entire audio folder will be deleted, including old files
##
recognizer = SpeechRecognition(
        API_KEY_LOCATION=os.path.join('../ExternalScripts/_key', 'GAPI.json'),
        save_audio_files=True
)

###
# Streaming recognition test.
# Streams audio to Google Cloud until it has found a 'final' result.
# This method will block the current thread until there exists an item in the 'final_result_queue'
# and after it has found one and sent it to furhat, will stop recording.
#
# Note the creation of a thread for the async recognition.
##
active_thread = threading.Thread(target=recognizer.recognize_async_audio_stream, args=( "sv-SE" , ) )       
active_thread.start()
#while Speaking:
furhat.speak(recognizer.final_result_queue.get())
recognizer.stop_record_microphone()

#####

###
# Recording test.
# Recods a .wav file for around 10 seconds.
# This file will then be sent to Google Cloud by using the
# 'recognize_sync_audio_file' function.
#
# Note recognizer.get() function used to get the first recording of the current session.
# (False is used here as no await is needed.)
##
recognizer.start_record_microphone()
time.sleep(10)
recognizer.stop_record_microphone()
furhat.speak(
    recognizer.recognize_sync_audio_file(
        file='./audio/' + recognizer.get(False) + '.raw',
        language_code="sv-SE"
    ))
```
