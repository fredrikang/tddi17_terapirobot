#!/usr/bin/python
import socket
import opencvwindow
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import  QWidget, QLabel, QApplication, QVBoxLayout, QPushButton
from PySide2.QtCore import QThread, Qt, Signal, Slot
from PySide2.QtGui import QImage, QPixmap

#from PyQt5.QtWidgets import  QWidget, QLabel, QApplication, QVBoxLayout, QPushButton
#from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
#from PyQt5.QtGui import QImage, QPixmap
import cv2
import sys

from furhatsocket import FurhatInterface

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

class Button(QPushButton):
    def __init__(self, text):
        super().__init__(text)




app = App([])
cvVideo = opencvwindow.OpenCVWindow()
button = Button("Hej")
app.addWidget(button)
app.addWidget(cvVideo)

furhat = FurhatInterface("TestingFurhat", "192.168.137.1")

defaultPhrasesFile = open('defaultphrases.txt', 'r')
defaultPhrases = defaultPhrasesFile.readlines()
#defaultPhrases = [ "Hej", "Ja", "Nej" ]

for phrase in defaultPhrases:
    phrase = phrase.strip()
    b = Button(phrase)
    b.clicked.connect(lambda: furhat.speak(phrase))
    app.addWidget(b)

app.run()