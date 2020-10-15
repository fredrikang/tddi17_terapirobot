#!/usr/bin/python
import socket
import opencvwindow
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import  QWidget, QLabel, QApplication, QVBoxLayout, QPushButton
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
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

    @pyqtSlot(QWidget)
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
app.run()