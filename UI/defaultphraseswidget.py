#!/usr/bin/python

from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from flowlayout import *

class DefaultPhrasesWidget(QWidget):
    def __init__(self, furhat):
        super().__init__()
        self.furhat = furhat
        self.title = 'Standard phrases'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.scroller = ScrollingFlowWidget(self)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.scroller)

    def addButton(self, buttonLabel, textToSay):
        b = QPushButton(buttonLabel)
        b.clicked.connect(lambda state = False: self.furhat.speak(textToSay))
        b.setToolTip(textToSay)
        self.scroller.addWidget(b)

    def addPhrases(self, phrases):
        for phrase in phrases:
            fras = phrase.strip()
            result = phrase.find(':')
            self.addButton(phrase[0:result], fras[result+1:])

