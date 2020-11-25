#!/usr/bin/python
import socket
import opencvwindow
import furhatvideo
import subprocess
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import cv2
import sys

class App(QApplication):
    def __init__(self, stringArray):
        super().__init__(stringArray)
        self.initLayout()
        self.initWindow()

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

app.addWidget(menuButtonHolder)
app.addWidget(videoHolder)
app.setStyle("Fusion")
app.run()
