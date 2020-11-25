#!/usr/bin/python
import socket
import opencvwindow
import subprocess
import os, sys

from threading import Thread
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import  QWidget, QLabel, QApplication, QVBoxLayout, QPushButton
from PySide2.QtCore import QThread, Qt, Signal, Slot
from PySide2.QtGui import QImage, QPixmap
sys.path.insert(1, '../ExternalScripts/SpeechRecognition') 
from speechrecognition import SpeechRecognition
#from PyQt5.QtWidgets import  QWidget, QLabel, QApplication, QVBoxLayout, QPushButton
#from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
#from PyQt5.QtGui import QImage, QPixmap
import cv2
import sys

class App(QApplication):
    def __init__(self, stringArray):
        super().__init__(stringArray)
        self.initLayout()
        self.initWindow()
        self.recognizer = SpeechRecognition(
            API_KEY_LOCATION=os.path.join('../ExternalScripts/_key', 'GAPI.json'), 
            save_audio_files=True
        )
        #self.recognizer.debug=False # disable printing to terminal


    def initLayout(self):
        self.layout = QVBoxLayout()

    def initWindow(self):
        self.window = QWidget()
        self.window.setLayout(self.layout)

    @Slot(QWidget)
    def addWidget(self, widget):
        self.layout.addWidget(widget)

    def addWidgets(self, widgets):
        for w in widgets:
            self.addWidget(w)

    def run(self):
        self.window.show()
        super().exec_()

    def startSpeechRecognition(self):
        active_thread = Thread(target=self.recognizer.recognize_async_audio_stream, args=( "sv-SE" , ) )       
        active_thread.start()
        print(self.recognizer.final_result_queue.get())
        self.recognizer.stop_record_microphone()
        active_thread.join()

class Button(QPushButton):
    def __init__(self, text):
        super().__init__(text)




app = App([])
cvVideo = opencvwindow.OpenCVWindow()
button = QPushButton("Open LogViewer")
speechButton = QPushButton("Speak")
speechButton.clicked.connect(app.startSpeechRecognition)
button.clicked.connect(lambda: subprocess.Popen(['../ExternalScripts/LogScripts/LogViewer/run_linux.sh']))
app.addWidget(button)
app.addWidget(speechButton)
app.addWidget(cvVideo)
app.run()