# This Python file uses the following encoding: utf-8
import sys
import mainwindow
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QFile, QIODevice
from furhatinterface import FurhatInterface
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--ip', type=str, help='ip address of the robot', required=True)
    args = parser.parse_args()
    app = QApplication(sys.argv)
    furhat = FurhatInterface("FurhatUIClient", args.ip)
    window = mainwindow.MainWindow(app, furhat)
    window.addDefaultPhraseButtons()
    window.addGestureButtons()
    window.addStates()
    window.addChangeModeButton()
    window.addVideoStream(args.ip)
    window.setup_log()
    window.setupSendButton()
    window.setupSpeech()
    window.show()
    sys.exit(app.exec_())