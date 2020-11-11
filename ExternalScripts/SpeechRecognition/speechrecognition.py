import shutil
import os
import io
import queue
import json
import grpc

from microphonehandler import MicrophoneHandler
from google.cloud import speech
from google.protobuf.json_format import MessageToDict, MessageToJson

class SpeechRecognition:
    """
    Represents a Speech Recognition handler. 
    This allows for recording microphone audio, stopping the recording and 
    sending a request to Google Cloud services for a Speech To Text action.

    Files will be saved in the preffered_audio_folder or in the default ./audio folder.
    If save_audio_files is False all recorded audio will be deleted on destruction of this object.
    The microphone recording is handled in its own thread by using the MicrophoneHandler.
   
    Args:   
        API_KEY_LOCATION -- path to the API KEY json file
        preffered_audio_folder -- preffered folder for recorded audio files (defaults to ./audio)
        save_audio_files -- save audio files after program is finished if True else remove all recorded files.
    """
    def __init__(self, API_KEY_LOCATION, preffered_audio_folder = None, save_audio_files = False):
        # Set environment variable.
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = API_KEY_LOCATION
        
        self.current_session    = []    
        self.record_length      = 0
        self.save_audio_file    = save_audio_files
        self.client             = speech.SpeechClient()
        self.final_result_queue = queue.Queue() # Used to store all streamed transcriptions for most recent session.

        if (preffered_audio_folder == None):
            self.audio_file_folder = './audio'
        else:
            self.audio_file_folder = preffered_audio_folder

        self.microphone_handler = MicrophoneHandler(self.audio_file_folder)

        # If any language isn't here add it to enable support for it or load from text file (the recognizer will check if the language is present here)
        # See all supported languages on: https://cloud.google.com/speech-to-text/docs/languages
        self.languages = [
            'ca-ES', 'my-MM', 'hr-HR',
            'da-DK', 'nl-BE', 'en-US',
            'fi-FI', 'fr-FR', 'de-AT',
            'de-DE', 'sv-SE', 'no-NO'          
        ]

    
    def load_language_codes(self, path):
        """
        Load language codes from a text file (formatted one code per line).

        Args:
            path -- path to language code file.
        """    
        try:
            fp = open(path, 'r+')
            languages = [line for line in fp.readlines()]
            fp.close
        except:
            print('Failed to read languages file.')
            return
        
        self.languages = languages

    def start_record_microphone(self):
        """
        Start recording from microphone.
        Will create a audio folder to save the recorded files.
        The files will be removed in the deconstructor if specified.
        """
        if not os.path.exists(self.audio_file_folder):
            os.makedirs(self.audio_file_folder)

        self.microphone_handler.start_recording()
        self.current_session.append(self.microphone_handler.current_session)

    def stop_record_microphone(self):
        """
        Stop recording, saves audio file.

        Returns: 
            The filename of the audio file.
        """
        return self.microphone_handler.stop_recording()
                  
    def recognize_sync_audio_file(self, file, language_code = "en-US", is_long_recording = False):
        """
        Send audio through Google API for Speech To Text and return the string representation of the audio.

        Args:
            file -- the filepath to file for STT. 
            language_code  -- language to use for recognition. See languages for supported languages.   
        
        Returns:
            The transcript of the most likely translation.
        """
        with io.open(file, "rb") as audio_file:
            content = audio_file.read()
            audio = speech.RecognitionAudio(content=content)

        if language_code not in self.languages:
            print('\"{}\" is not a supported language code. Make sure it\'s supported by Google and try adding it to the languages list.\n'.format(language_code))
            return -1

        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=self.microphone_handler.RATE,
            language_code=language_code,
        )

        try:
            response = self.client.long_running_recognize(config=config, audio=audio, timeout=500).result()   
        except:
            return -1

        return self.__get_message_from_proto(response)['transcript']
    
    # pylint: disable=too-many-function-args
    def recognize_async_audio_stream(self, language_code = "en-US"):
        """
        Recognize in "real-time" from microphone stream.
        
        May be created as a thread of its own, otherwise the streaming must be 
        stopped with CTRL + C.
        
        Stores all decoded final text into `final_result_queue`.

        Args:
            language_code -- language to use for recognition. See languages for supported languages.   
        """      
        if language_code not in self.languages:
            print('\"{}\" is not a supported language code. Make sure it\'s supported by Google and try adding adding it to the languages list.\n'.format(language_code))
            return

        self.final_result_queue.queue.clear() # Clear all items in queue for new stream.

        config_stream = speech.StreamingRecognitionConfig(
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=self.microphone_handler.RATE,
                language_code=language_code,
            ),
            interim_results=True      
        )

        self.microphone_handler.start_recording(streaming=True)
        while self.microphone_handler.streaming:
            data = self.microphone_handler.stream_generator()
            requests = (speech.StreamingRecognizeRequest(audio_content=content) for content in data)

            try:
                responses = self.client.streaming_recognize(config_stream, requests)
                for response in responses:
                    if response.results[0].is_final:
                        self.final_result_queue.put(response.results[0].alternatives[0].transcript)
                    else:
                        print(response.results[0].alternatives[0].transcript + '\n') # Print all non final results (debug).
            except:
                print('Failed to get response.')

    def __clear_audio_files(self):
        """
        Clear all audio files from set audio folder.
        """
        try:
            shutil.rmtree(self.audio_file_folder)
        except:
            print('Failure to clear audio files in {self.audio_file_folder}')

    def __get_message_from_proto(self, message) -> dict: 
        """
        Decode and get the most confident message from the protobuf.

        Args:
            message -- the protobuf message received when translating.
        
        Returns:
            Dictionary containing transcript and confidence.
        """     
        result = { 'transcript' : '' , 'confidence' : 0.0 }
        try:          
            result = MessageToDict(message._pb)['results'][0]['alternatives'][0]
        except:
            result['transcript'] = ''
            result['confidence'] = 0.0
     
        return result

    def __del__(self):
        """
        Deconstructor.
        Stop recording and remove all audio files if save_audio_file is False
        """      
        self.stop_record_microphone()
        
        if not self.save_audio_file:
            self.__clear_audio_files()       