#!/usr/bin/python
import socket
import opencvwindow
import defaultphraseswidget
import furhatvideo
import subprocess
import os

from threading import Thread
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import cv2
import sys

from furhatinterface import FurhatInterface

class App(QApplication):
    def __init__(self, stringArray):
        super().__init__(stringArray)
        self.initLayout()
        self.initWindow()
        self.recognizer = SpeechRecognition(
            API_KEY_LOCATION=os.path.join('../ExternalScripts/_key', 'GAPI.json'), 
            save_audio_files=True
        )
        #self.recognizer.debug=False # disable "on-the-fly" printing to terminal
    
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

    ## No extra thread needed!
    def startSpeechRecognition(self):
        active_thread = Thread(target=self.recognizer.recognize_async_audio_stream, args=( "sv-SE" , ) )       
        active_thread.start()
        furhat.speak(self.recognizer.final_result_queue.get())
        self.recognizer.stop_record_microphone()
        active_thread.join()

def menuButton(button):
    button.setFixedSize(150, 50)
    button.move(100, 100)
    



app = App([])
#cvVideo = opencvwindow.OpenCVWindow()
fVideoWindow = furhatvideo.FurhatVideoWindow()

videolayout = QVBoxLayout()
videolayout.addWidget(fVideoWindow)

videoHolder = QWidget()
videoHolder.setFixedSize(1800,1200)
videoHolder.setLayout(videolayout)

startRecording = QPushButton("start")
stopRecording = QPushButton("stop")
button = QPushButton("CameraFeedToggle")

openLogViewerButton = QPushButton("LogViewer")
startSpeakButton = QPushButton("Speak")

startSpeakButton.clicked.connect(app.startSpeechRecognition)
openLogViewerButton.clicked.connect(lambda: subprocess.Popen(['../ExternalScripts/LogScripts/LogViewer/run_linux.sh'])) # Se över path vid implementationen.

button.clicked.connect(lambda: videoHolder.setVisible(not videoHolder.isVisible()))
startRecording.clicked.connect(lambda: fVideoWindow.StartRecording("recordingTest"))
stopRecording.clicked.connect(lambda: fVideoWindow.StopRecording())


#button.clicked.connect(lambda: videoHolder.setVisible(not videoHolder.isVisible()))

menuButton(button)
menuButtonlayout = QVBoxLayout()
menuButtonlayout.addWidget(button)

menuButton(startRecording)
menuButtonlayout.addWidget(startRecording)

menuButton(stopRecording)
menuButtonlayout.addWidget(stopRecording)

menuButtonHolder = QWidget()
menuButtonHolder.setFixedSize(200,150)
menuButtonHolder.setLayout(menuButtonlayout)

furhat = FurhatInterface("TestingFurhat", "192.168.137.1")

defaultPhrasesWidget = defaultphraseswidget.DefaultPhrasesWidget(furhat)

defaultPhrasesFile = open('defaultphrases.txt', 'r')
defaultPhrases = defaultPhrasesFile.readlines()
defaultPhrasesWidget.addPhrases(defaultPhrases)

app.addWidget(defaultPhrasesWidget)

changemodebutton = QPushButton("ändra läge")
changemodebutton.clicked.connect(lambda: furhat.changemode())
app.addWidget(changemodebutton)

app.addWidget(menuButtonHolder)
app.addWidget(videoHolder)

app.addWidget(openLogViewerButton)
app.addWidget(startSpeakButton)

app.setStyle("Fusion")
app.run()
