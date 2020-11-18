import cv2
import zmq
import io
import numpy as np
from docopt import docopt
import pyaudio
import wave
import socket
import threading
import time
import ffmpeg
import os
from PySide2.QtWidgets import  QWidget, QLabel, QApplication
from PySide2.QtCore import QThread, Qt, Signal, Slot
from PySide2.QtGui import QImage, QPixmap
import sys

class FurhatVideoThread(QThread):
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

class FurHatStream:
    def __init__(self, host, size, record_output):
        self.size = size
        self.record_output = record_output
        #Testing facial recongintion
        context = zmq.Context()
        host = 'tcp://{0}:3000'.format(host)
        print('Setting host to: {0}'.format(host))
        print('Setting size to: {0}'.format(size))
        if record_output:
            print('Setting output file to: {0}'.format(record_output))
        else:
            print('No recording will be made')

        self.footage_socket = context.socket(zmq.SUB)
        self.footage_socket.setsockopt_string(zmq.SUBSCRIBE, u"")
        self.footage_socket.setsockopt(zmq.RCVHWM, 1)
        self.footage_socket.setsockopt(zmq.CONFLATE, 1)
        
        self.footage_socket.connect(host)
        if record_output:
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            self.video_writer = cv2.VideoWriter(record_output, fourcc, 10, self.size)
       
    def run(self):
       print('Listening to camera stream')
        global stop_threads
        while not stop_threads:
            frame = self.footage_socket.recv()
            imgBuff = np.frombuffer(frame, dtype=np.uint8)
            #print(imgBuff)
            img = cv2.imdecode(imgBuff, cv2.IMREAD_COLOR)
            img = cv2.resize(img, self.size, interpolation = cv2.INTER_AREA)
            if self.record_output:
                self.video_writer.write(img)
            #cv2.imshow("FurHatStream", img)
            #cv2.waitKey(1)

        if self.record_output:
            self.video_writer.release()
        cv2.destroyAllWindows()  

def run_stream(host, width, height, record_output):
	stream = FurHatStream(host=host, size=(int(width), int(height)), record_output=record_output)
	stream.run()