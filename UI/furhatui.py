#!/usr/bin/python
import socket
import opencvwindow
import defaultphraseswidget
import furhatvideo
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

def turnOffVideo(widget):
    widget.setVisible(not widget.isVisible())


def menuButton(button):
    button.setFixedSize(150, 50)
    button.move(100, 100)
    



app = App([])
cvVideo = opencvwindow.OpenCVWindow()
#furhatstream = furhatvideo.FurHatStream(host="192.168.43.131", size=(int(640), int(480)), record_output="")

videolayout = QVBoxLayout()
videolayout.addWidget(cvVideo)

videoHolder = QWidget()
videoHolder.setFixedSize(1800,1200)
videoHolder.setLayout(videolayout)

button = QPushButton("CameraFeedToggle")
button.clicked.connect(lambda: widget.setVisible(not widget.isVisible()))

menuButton(button)
menuButtonlayout = QVBoxLayout()
menuButtonlayout.addWidget(button)

menuButtonHolder = QWidget()
menuButtonHolder.setFixedSize(200,150)
menuButtonHolder.setLayout(menuButtonlayout)

furhat = FurhatInterface("TestingFurhat", "192.168.137.1")

defaultPhrasesFile = open('defaultphrases.txt', 'r')
defaultPhrases = defaultPhrasesFile.readlines()
defaultPhrasesWidget = defaultphraseswidget.DefaultPhrasesWidget(furhat)

for phrase in defaultPhrases:
    fras = phrase.strip()
    result = phrase.find(':')
    defaultPhrasesWidget.addButton(phrase[0:result], fras[result+1:])

app.addWidget(defaultPhrasesWidget)

changemodebutton = QPushButton("ändra läge")
changemodebutton.clicked.connect(lambda: furhat.changemode())
app.addWidget(changemodebutton)

app.addWidget(menuButtonHolder)
app.addWidget(videoHolder)
app.setStyle("Fusion")
app.run()
