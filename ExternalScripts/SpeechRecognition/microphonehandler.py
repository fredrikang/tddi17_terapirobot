import pyaudio
import wave
import datetime
import time
import os
import sys
import queue
from threading import Thread

class MicrophoneHandler:
    """
    Represents a microphone handler for recording and saving audio recorded.
    Uses PyAudio to record audio and stores the recorded files which will be saved
    and named in the format specified by the caller. 
    If no specification is made it will default to a timestamp. 

    As the recording starts a new thread the created object should not go out of scope
    unless intended to do so.
     
    Args:
        audio_folder -- folder to store recorded audio in.  
    """
    def __init__(self, audio_folder):
        self.CHUNK     = 1024
        self.FORMAT    = pyaudio.paInt16  
        self.RATE      = 44100
        self.CHANNELS  = 1
        self.EXTENSION = '.raw'

        self.recording       = False
        self.streaming       = False
        self.chunk_buf       = queue.Queue()
        self.current_session = None
        self.audio_folder    = audio_folder
        self.paudio          = pyaudio.PyAudio()
        
        self._stream = None
        self.__active_thread = None
       
    def start_recording(self, filename = None, streaming = False):
        """
        Starts recording the default microphone.
        Creates a new thread for recording audio.
        Currently only supports one thread, any more may cause issues.

        Args:
            filename  -- filename of current recording, if None it will default to a timestamp.
            streaming -- if true will stream asynchronous audio for recognition. If false will create a audio file and send it for recognition.
        """
        if (self.paudio.get_device_count() < 1):
            print('Failed to identify any microphone!')
            return

        if filename is None:
            filename = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H-%M-%S')

        self.current_session = filename
        if self.__active_thread is not None:
            self.stop_recording
       
        if streaming:
            #self.__active_thread = Thread(target=self.__active_streaming, args=( filename, ) )          
            self.__active_streaming(filename)
        else:
            self.__active_thread = Thread(target=self.__active_recording, args=( filename, ) )       
            self.__active_thread.start()
        
    def stop_recording(self):
        """
        Stops recording and waits for the recorder thread to finish.
        Returns the filename of the new audio file.
        """
        print('Stopping recording.')
        self.recording = False        
        
        if self.__active_thread != None:
            self.__active_thread.join()
        
        if self.streaming:
            self._stream.stop_stream()
            self._stream.close()
            self.paudio.terminate()

        self.streaming = False
        self.recording = False

        self.__active_thread = None   
        
        return self.current_session

    def _audio_callback_handler(self, in_data, *args, **kwargs):
        """ 
        Collect and store data from Microphone 
        """
        self.chunk_buf.put(in_data)
        return None, pyaudio.paContinue

    def __active_recording(self, filename):
        """
        Record function for the active recorder thread.

        Args:
            filename -- name for the recorded audio file.
        """
        print('Recording: {}'.format(filename))
        try:
            self._stream = self.paudio.open(
                format             = self.FORMAT,
                channels           = self.CHANNELS,
                rate               = self.RATE,
                input              = True,
                input_device_index = self._get_default_microphone(),
                frames_per_buffer  = self.CHUNK
            )
        except: 
            sys.sterr.write("Failed to open audio stream.")
            return

        self.recording = True       
        frames = []
        try:
            while(self.recording is True):
                data = self._stream.read(self.CHUNK)
                frames.append(data)
        except:
            sys.stderr.write("Error when recording audio.")

        self._stream.stop_stream()
        self._stream.close()
        self.paudio.terminate()

        try:          
            file = wave.open(os.path.join(self.audio_folder, filename) + self.EXTENSION, 'wb')
            file.setnchannels(self.CHANNELS)
            file.setsampwidth(self.paudio.get_sample_size(self.FORMAT))
            file.setframerate(self.RATE)
            file.writeframesraw(b''.join(frames))
        except:
            print('Failure to write file {}{}'.format(filename, self.EXTENSION))
        finally:
            file.close()

    def __active_streaming(self, filename = None):
        """
        Streaming function for the active recorded thread.

        Args:
            filename -- OPTIONAL.
        """
        self.recording = True
        print('Streaming: {}'.format(filename))
        try:
            self._stream = self.paudio.open(
                format             = self.FORMAT,
                channels           = self.CHANNELS,
                rate               = self.RATE,
                input              = True,
                input_device_index = self._get_default_microphone(),
                frames_per_buffer  = self.CHUNK,
                stream_callback    = self._audio_callback_handler,
            )
        except: 
            print('Failed to open audio stream.')
            return

        self.streaming = True
        self._stream.start_stream()
        
    def stream_generator(self):
        """
        Yield all currently recorded chunks of audio.
        """
        while self.streaming:
            chunk = self.chunk_buf.get()
            if chunk is None:
                return
            data = [chunk]

            while True:
                try:
                    chunk = self.chunk_buf.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)

                except queue.Empty:
                    break
            
            yield b''.join(data)

    def _get_default_microphone(self) -> int:
        try:        
            p = pyaudio.PyAudio()
            return p.get_default_input_device_info()['index']
        except:
            return 0