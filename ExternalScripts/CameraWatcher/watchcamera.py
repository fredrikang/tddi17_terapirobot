"""Usage: 
    watchcamera.py [-o FILE] [--width=WIDTH] [--height=HEIGHT] HOST

Example, try:
    watchcamera.py 127.0.0.1
    watchcamera.py -o output.avi 127.0.0.1
    watchcamera.py --width=1920 --height=1080 -o output.avi 127.0.0.1

Options:
    -h --help                   show this
    -o FILE, --output FILE      filename of recording, if not provided no recording will be made.
    --width=WIDTH               width of the stream [default: 800]
    --height=HEIGHT             height of the stream [default: 600]

"""

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

class MicrophoneStream: 

    BUFFER_SIZE = 1024

    def __init__(self, host, record_output):
        self.audio_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.audio_socket.connect((host, 8887))
        self.record_output = record_output

        wave_obj = wave.open(self.audio_socket.makefile(mode='rb'), 'rb')

        p = pyaudio.PyAudio()
        self.speaker_stream = p.open(format   = p.get_format_from_width(wave_obj.getsampwidth()),
                                    channels = wave_obj.getnchannels(),
                                    rate     = wave_obj.getframerate(),
                                    output   = True)
        if record_output:
            self.audio_writer = wave.open(record_output, 'wb')
            self.audio_writer.setparams(wave_obj.getparams())

    def run(self):
        print('Listening to microphone stream')
        global stop_threads
        while not stop_threads:
            data = self.audio_socket.recv(self.BUFFER_SIZE)
            self.speaker_stream.write(data)

            if self.record_output:
                self.audio_writer.writeframesraw(data)

        if self.record_output:
            self.audio_writer.close()

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
            cv2.imshow("FurHatStream", img)
            cv2.waitKey(1)

        if self.record_output:
            self.video_writer.release()
        cv2.destroyAllWindows()  

def run_stream(host, width, height, record_output):
    stream = FurHatStream(host=host, size=(int(width), int(height)), record_output=record_output)
    stream.run()

def run_microphone_stream(host, record_output):
    stream = MicrophoneStream(host=host, record_output=record_output)
    stream.run()

if __name__ == '__main__':
    arguments = docopt(__doc__, version='Furhat camerastreamer v.1')
    record_output = arguments["--output"]
    host = arguments["HOST"]
    width = arguments["--width"]
    height = arguments["--height"]

    print('To exit close this script with Ctrl+C')

    print('Starting camera thread')
    record_output_cam = None
    if record_output:
        record_output_cam = "temp_cam.avi"
    cam_stream_thread = threading.Thread(target=run_stream, args=(host, width, height, record_output_cam))
    cam_stream_thread.start()

    print('Starting microphone thread')
    record_output_mic = None
    if record_output:
        record_output_mic = "temp_mic.wav"
    mic_stream_thread = threading.Thread(target=run_microphone_stream, args=(host, record_output_mic))
    mic_stream_thread.start()

    stop_threads = False
    try:
        while True:
            time.sleep(0.001)
    except KeyboardInterrupt:
        stop_threads = True

        # Wait until the threads have finished running
        cam_stream_thread.join()
        mic_stream_thread.join()

        if record_output:
            # Merge audio and video into record_output
            video = ffmpeg.input(record_output_cam)
            audio = ffmpeg.input(record_output_mic)
            output = ffmpeg.output(video, audio, record_output, vcodec='copy', acodec='aac')
            output.run(overwrite_output=True)

            # Remove the temporary audio and video files
            os.remove(record_output_cam)
            os.remove(record_output_mic)
