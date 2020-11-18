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
    record_output = False
    def StartStream(self, host):
        context = zmq.Context()
        host = 'tcp://{0}:3000'.format(host)
        print('Setting host to: {0}'.format(host))

        self.footage_socket = context.socket(zmq.SUB)
        self.footage_socket.setsockopt_string(zmq.SUBSCRIBE, u"")
        self.footage_socket.setsockopt(zmq.RCVHWM, 1)
        self.footage_socket.setsockopt(zmq.CONFLATE, 1)
        self.footage_socket.connect(host)
        
    def run(self):
        while True:
            frame = self.footage_socket.recv()
            imgBuff = np.frombuffer(frame, dtype=np.uint8)
            img = cv2.imdecode(imgBuff, cv2.IMREAD_COLOR)
            if self.record_output:
                self.video_writer.write(img)
            if True:
                # https://stackoverflow.com/a/55468544/6622587
                rgbImage = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)

        if self.record_output:
            StopRecording()

    def StartRecording(self):
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.video_writer = cv2.VideoWriter("temp_video_output.avi", fourcc, 10, (640,480))
        self.record_output = True

    def StopRecording(self):
        self.record_output = False
        self.video_writer.release()

class FurhatAudioStream(QThread):
    BUFFER_SIZE = 1024
    record_output = False
    def StartStream(self, host):
        self.audio_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.audio_socket.connect((host, 8887))
        self.wave_obj = wave.open(self.audio_socket.makefile(mode='rb'), 'rb')
        p = pyaudio.PyAudio()
        self.speaker_stream = p.open(format   = p.get_format_from_width(self.wave_obj.getsampwidth()),
                                     channels = self.wave_obj.getnchannels(),
                                     rate     = self.wave_obj.getframerate(),
                                     output   = True)

    def StartRecording(self):
        self.audio_writer = wave.open("temp_audio_output.wav", 'wb')
        self.audio_writer.setparams(self.wave_obj.getparams())
        self.record_output = True

    def StopRecording(self):
        self.record_output = False
        self.audio_writer.close()

    def run(self):
        while True:
            data = self.audio_socket.recv(self.BUFFER_SIZE)
            self.speaker_stream.write(data)

            if self.record_output:
                self.audio_writer.writeframesraw(data)

        if self.record_output:
            self.audio_writer.close()

class FurhatVideoWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'FurHatStream'
        self.left = 100
        self.top = 100
        self.width = 640
        self.height = 480
        self.nameOfFile = None
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
        self.vth = FurhatVideoThread(self)
        self.vth.StartStream("192.168.43.131")
        self.vth.changePixmap.connect(self.setImage)
        self.vth.start()
        self.ath = FurhatAudioStream(self)
        self.ath.StartStream("192.168.43.131")
        self.ath.start()

    def StartRecording(self, name):
        self.ath.StartRecording()
        self.vth.StartRecording()
        self.nameOfFile = name
        
    def StopRecording(self):
        if self.nameOfFile:
            print("stopped _ " + self.nameOfFile)
            self.ath.StopRecording()
            self.vth.StopRecording()
            print("stopped _ 1")

            th = CombineAudioVideoThread(self)
            th.nameOfFile = self.nameOfFile
            print("stopped _ 2")

            th.start()
            

class CombineAudioVideoThread(QThread):
    nameOfFile = None
    def run(self):
        video = ffmpeg.input("temp_video_output.avi")
        audio = ffmpeg.input("temp_audio_output.wav")
        print("stopped _ 3")

        output = ffmpeg.output(video, audio, self.nameOfFile, vcodec='copy', acodec='aac')
        print("stopped _ 4")

        output.run(overwrite_output=True) #This crashed the whole UI
        print("stopped _ 5")

        # Remove the temporary audio and video files
        os.remove("temp_audio_output.wav")
        os.remove("temp_video_output.avi")