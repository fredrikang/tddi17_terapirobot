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
from PySide2.QtWidgets import  QWidget, QLabel, QApplication, QVBoxLayout, QHBoxLayout, QSizePolicy, QPushButton, QDialog, QFileDialog
from PySide2.QtCore import QThread, Qt, Signal, Slot, QSize, QDir
from PySide2.QtGui import QImage, QPixmap
import sys

class FurhatVideoThread(QThread):
    changePixmap = Signal(QImage)
    record_output = False
    def StartStream(self, host):
        context = zmq.Context()
        host = 'tcp://{0}:3000'.format(host)
        print('Setting ZMQ host to: {0}'.format(host))

        self.footage_socket = context.socket(zmq.SUB)
        self.footage_socket.setsockopt_string(zmq.SUBSCRIBE, u"")
        self.footage_socket.setsockopt(zmq.RCVHWM, 1)
        self.footage_socket.setsockopt(zmq.CONFLATE, 1)
        self.footage_socket.connect(host)
        self.enabled = True
        
    def run(self):
        print('Listening to camera stream')
        while self.enabled:
            frame = self.footage_socket.recv()
            imgBuff = np.frombuffer(frame, dtype=np.uint8)
            img = cv2.imdecode(imgBuff, cv2.IMREAD_COLOR)
            if self.record_output:
                self.video_writer.write(img)
            if self.enabled:
                rgbImage = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)

        if self.record_output:
            self.StopRecording()

    def stop(self):
        self.enabled = False

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
        self.isMuted = False
        self.enabled = True

    def StartRecording(self):
        self.audio_writer = wave.open("temp_audio_output.wav", 'wb')
        self.audio_writer.setparams(self.wave_obj.getparams())
        self.record_output = True

    def StopRecording(self):
        self.record_output = False
        self.audio_writer.close()

    def run(self):
        while self.enabled:
            data = self.audio_socket.recv(self.BUFFER_SIZE)
            if not self.isMuted:
                self.speaker_stream.write(data)

            if self.record_output:
                self.audio_writer.writeframesraw(data)

        if self.record_output:
            self.audio_writer.close()

    def stop(self):
        self.enabled = False

class FurhatVideoAudioWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.videoWindow = FurhatVideoAudioWidgetStream()
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.videoWindow.sizePolicy().hasHeightForWidth())
        self.videoWindow.setSizePolicy(sizePolicy)
        self.videoWindow.setMinimumSize(QSize(640, 480))
        self.videoWindow.setMaximumSize(QSize(640, 480))
        self.videoWindow.setObjectName("videoWindow")
        self.layout.addWidget(self.videoWindow)
        self.button_layout = QHBoxLayout()
        self.layout.addLayout(self.button_layout)
        self.recordButton = QPushButton("Record")
        self.recordButton.clicked.connect(self.start_recording)
        self.button_layout.addWidget(self.recordButton)
        self.muteButton = QPushButton("Mute")
        self.muteButton.clicked.connect(self.mute)
        self.button_layout.addWidget(self.muteButton)
        self.isRecording = False
        
    
    def stop(self):
        self.videoWindow.ath.stop()
        self.videoWindow.vth.stop()


    def start_videostream(self, host : str):
        self.videoWindow.start_videostream(host)

    def start_audiostream(self, host : str):
        self.audioHost = host
        self.videoWindow.start_audiostream(host)

    def start_recording(self):
        if not self.isRecording:
            dialog = QFileDialog()
            dialog.setFilter(dialog.filter() | QDir.Hidden)
            dialog.setDefaultSuffix('avi')
            dialog.setAcceptMode(QFileDialog.AcceptSave)
            dialog.setNameFilters(['Video File (*.avi)'])
            if dialog.exec_() == QDialog.Accepted:
                fileName = dialog.selectedFiles()[0]
                self.videoWindow.StartRecording(fileName)
                self.recordButton.setText("Stop recording")
                self.isRecording = True
            else:
                print('Cancelled')

        else:
            self.videoWindow.StopRecording()
            self.recordButton.setText("Start recording")
            self.isRecording = False


    def StopRecording(self):
        self.videoWindow.StopRecording()

    def mute(self):
        if not self.videoWindow.ath.isMuted:
            self.videoWindow.ath.isMuted = True
            
        else:
            self.videoWindow.ath.isMuted = False


class FurhatVideoAudioWidgetStream(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'FurHatStream'
        self.width = 640
        self.height = 480
        self.nameOfFile = None
        self.initUI()

    @Slot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))

    def initUI(self):
        self.setWindowTitle(self.title)
        self.label = QLabel(self)
        self.label.resize(640, 480)

    def start_videostream(self, host : str):
        self.vth = FurhatVideoThread(self)
        self.vth.StartStream(host)
        self.vth.changePixmap.connect(self.setImage)
        self.vth.start()

    def start_audiostream(self, host : str):
        self.ath = FurhatAudioStream(self)
        self.ath.StartStream(host)
        self.ath.start()

    def StartRecording(self, name):
        self.ath.StartRecording()
        self.vth.StartRecording()
        self.nameOfFile = name
        
    def StopRecording(self):

        if self.nameOfFile:
            self.ath.StopRecording()
            self.vth.StopRecording()
            th = CombineAudioVideoThread(self)
            th.nameOfFile = self.nameOfFile
            th.start()
            

class CombineAudioVideoThread(QThread):
    nameOfFile = None
    def run(self):
        video = ffmpeg.input("temp_video_output.avi")
        audio = ffmpeg.input("temp_audio_output.wav")
        output = ffmpeg.output(video, audio, self.nameOfFile, vcodec='copy', acodec='aac')
        output.run(overwrite_output=True)


