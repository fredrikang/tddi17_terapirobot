import unittest
import os, sys, inspect

sys.path.append("..")

# pylint: disable=import-error
import SpeechRecognition

class TestRecognition(unittest.TestCase):   
    def test_speech_to_text(self):
        r = SpeechRecognition.SpeechRecognition(API_KEY_LOCATION=os.path.join('C:', 'Users', '46709', 'Downloads', 'GAPI.json'), save_audio_files=True)
        self.assertEqual(r.recognize_sync_audio_file('./audio/2020-10-21_17-38-31.raw'), 'hello hello hello hello hello hello')

    def test_faulty_language_code(self):
        r = SpeechRecognition.SpeechRecognition(API_KEY_LOCATION=os.path.join('C:', 'Users', '46709', 'Downloads', 'GAPI.json'), save_audio_files=True)
        self.assertEqual(r.recognize_sync_audio_file('./audio/2020-10-21_17-38-31.raw', "bad_code"), -1)

    ## Unstable test.
    def test_return_option_all(self):
        r = SpeechRecognition.SpeechRecognition(API_KEY_LOCATION=os.path.join('C:', 'Users', '46709', 'Downloads', 'GAPI.json'), save_audio_files=True)
        self.assertEqual(r.recognize_sync_audio_file('./audio/2020-10-21_17-38-31.raw', return_options="all"), 
"""results {
  alternatives {
    transcript: "hello hello hello hello hello hello"
    confidence: 0.987629
  }
}
""")


if __name__ == '__main__':
    unittest.main()