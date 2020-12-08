#!/usr/bin/python

from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from flowlayout import *

class StateButtonsWidget(QWidget):
    def __init__(self, furhat):
        super().__init__()
        self.furhat = furhat
        self.title = 'States'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.scroller = ScrollingFlowWidget(self)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.scroller)

    def addButton(self, buttonLabel, stateToEnter):
        b = QPushButton(buttonLabel)
        b.setContentsMargins(5,5,5,5)
        b.clicked.connect(lambda state = False: self.furhat.goto(stateToEnter))
        b.setToolTip(stateToEnter)
        self.scroller.addWidget(b)

    def addStates(self, states):
        for entry in states:
            state = entry.strip()
            result = entry.find(':')
            self.addButton(entry[0:result], state[result+1:])

