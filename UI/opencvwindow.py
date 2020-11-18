#!/usr/bin/python

from PySide2.QtWidgets import  QWidget, QLabel, QApplication
from PySide2.QtCore import QThread, Qt, Signal, Slot
from PySide2.QtGui import QImage, QPixmap
import cv2
import sys

class OpenCVWindowThread(QThread):
    changePixmap = Signal(QImage)

    def run(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if ret:
                # https://stackoverflow.com/a/55468544/6622587
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)


class OpenCVWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Webcam'
        self.left = 100
        self.top = 100
        self.width = 640
        self.height = 480
        self.initUI()

    @Slot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.resize(1800, 1200)
        self.setStyleSheet("border: 2px solid black;")
        self.label = QLabel(self)
        self.label.move(280, 120)
        self.label.resize(640, 480)
        th = OpenCVWindowThread(self)
        th.changePixmap.connect(self.setImage)
        th.start()
