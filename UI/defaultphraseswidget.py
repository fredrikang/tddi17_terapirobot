#!/usr/bin/python

from PySide2.QtWidgets import *
from PySide2.QtCore import QThread, Qt, Signal, Slot
from PySide2.QtGui import QImage, QPixmap
import sys

class DefaultPhrasesWidget(QGroupBox):
    def __init__(self, furhat):
        super().__init__()
        self.furhat = furhat
        self.title = 'Standardfraser'
        self.left = 100
        self.top = 100
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.resize(1800, 1200)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

    def addButton(self, buttonLabel, textToSay):
        b = QPushButton(buttonLabel)
        b.clicked.connect(lambda state = False: self.furhat.speak(textToSay))
        b.setToolTip(textToSay)
        self.layout.addWidget(b)

    def addPhrases(self, phrases):
        for phrase in phrases:
            fras = phrase.strip()
            result = phrase.find(':')
            self.addButton(phrase[0:result], fras[result+1:])

