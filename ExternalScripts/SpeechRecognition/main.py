from speechrecognition import SpeechRecognition
import time
import os
from threading import Thread

recognizer = SpeechRecognition(
        API_KEY_LOCATION=os.path.join('../_key', 'GAPI.json'), 
        save_audio_files=True
)

# Create thread for async recognition.
# Use thread for not stalling main thread and allow for better control.
active_thread = Thread(target=recognizer.recognize_async_audio_stream, args=( "sv-SE" , ) )       
active_thread.start()
while True:
# Wait for a transcribed result.
        print('Final: {}'.format(recognizer.final_result_queue.get()))

# Stop microphone stream.
recognizer.stop_record_microphone()

#print(recognizer.recognize_sync_audio_file(file='./audio/' + '2020-10-21_17-38-31.raw', language_code="en-US", return_options=None))