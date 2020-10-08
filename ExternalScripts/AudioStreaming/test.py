import pyaudio
import wave
import socket


class MicrophoneStream: 

    BUFFER_SIZE = 1024

    def __init__(self, address, record):
        self.audio_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.audio_socket.connect(address)
        self.record = record

        wave_obj = wave.open(self.audio_socket.makefile(), 'rb')

        p = pyaudio.PyAudio()
        self.speaker_stream = p.open(format   = p.get_format_from_width(wave_obj.getsampwidth()),
                                     channels = wave_obj.getnchannels(),
                                     rate     = wave_obj.getframerate(),
                                     output   = True)
        if record:
            self.audio_writer = wave.open("output.wav", 'wb')
            self.audio_writer.setparams(wave_obj.getparams())

    def run(self):
        while True:
            try:
                data = self.audio_socket.recv(self.BUFFER_SIZE)
                self.speaker_stream.write(data)

                if self.record:
                    self.audio_writer.writeframesraw(data)

            except KeyboardInterrupt:
                if self.record:
                    self.audio_writer.close()
                break


stream = MicrophoneStream(address = ('127.0.0.1', 8887), record = False)
stream.run()