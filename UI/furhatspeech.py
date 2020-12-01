from PySide2.QtWidgets import  QWidget, QLabel, QPushButton
from PySide2.QtCore import QThread, Qt, Signal, Slot
from PySide2.QtGui import QImage, QPixmap
from speechrecognition import SpeechRecognition
import os

class FurhatSpeechAsyncThread(QThread):
    def __init__(self, recognizer, listening):
        super().__init__()
        self.recognizer = recognizer
        self.listening = listening
    def run(self):
        self.recognizer.recognize_async_audio_stream("sv-SE")
    

class FurhatSpeechThread(QThread):
    signal = Signal(str)
    def __init__(self, recognizer, furhat, listening):
        super().__init__()
        self.recognizer = recognizer
        self.furhat = furhat
        self.listening = listening
    def run(self):
        while True:
            res = self.recognizer.final_result_queue.get()
            text = res.alternatives[0].transcript
            self.signal.emit(text)
            if res.is_final:
                break
            
        self.listening = False 
        #self.signal.emit(text)           
        print('Final: {}'.format(text))
        self.furhat.speak(text)
        self.recognizer.stop_record_microphone()
        self.signal.emit("")


class FurhatSpeechWidget(QPushButton):
    def __init__(self, furhat, textBox):
        super().__init__("Microphone")
        recognizer = SpeechRecognition(
        API_KEY_LOCATION=os.path.join('../_key','GAPI.json'), 
        save_audio_files=True)
        self.listening = False
        self.speech_async_thread = FurhatSpeechAsyncThread(recognizer, self.listening )
        self.speech_thread = FurhatSpeechThread(recognizer, furhat, self.listening)

        self.clicked.connect(lambda state = False: self.toggle_listen())
        self.speech_thread.signal.connect(self.setTextBoxText)
        self.editText = textBox
    
    @Slot(str)
    def setTextBoxText(self, text):
        self.editText.setPlainText(text)

    def print_to_textbox(self, text):
        self.textBox.setPlainText(text)

    def toggle_listen(self):
        self.speech_async_thread.listening = True
        self.speech_async_thread.start()
        self.speech_thread.start()
        #print(self.speech_thread.listening)