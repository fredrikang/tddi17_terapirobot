#!/usr/bin/python

from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from flowlayout import *

class GesturesWidget(QWidget):
    def __init__(self, furhat):
        super().__init__()
        self.furhat = furhat
        self.title = 'Gestures'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.scroller = ScrollingFlowWidget(self)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.scroller)

    def addButton(self, buttonLabel, gesture):
        b = QPushButton(buttonLabel)
        b.clicked.connect(lambda state = False: self.furhat.gesture(gesture))
        b.setToolTip(buttonLabel)
        self.scroller.addWidget(b)

    def addGestures(self, gestures):
        for phrase in gestures:
            fras = phrase.strip()
            result = phrase.find(':')
            self.addButton(phrase[0:result], fras[result+1:])

