# This Python file uses the following encoding: utf-8
import sys
import mainwindow
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtCore import QFile, QIODevice
from furhatinterface import FurhatInterface
from furhatvideo import FurhatVideoWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = mainwindow.MainWindow()
    furhat = FurhatInterface("TestingFurhat", "192.168.43.131")
    #furhat.start_skill("Therapist-all")
    window.addDefaultPhraseButtons(furhat)
    window.addVideoStream("192.168.43.131")
    window.setup_log(furhat)
    window.setupSendButton(furhat)
    window.show()
    sys.exit(app.exec_())