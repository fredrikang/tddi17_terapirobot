# This Python file uses the following encoding: utf-8
import sys
import mainwindow
sys.path.append('../')
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtCore import QFile, QIODevice
from furhatinterface import FurhatInterface

if __name__ == "__main__":
    furhat = FurhatInterface("TestingFurhat", "localhost")
    furhat.start_skill("Therapist-all")

    app = QApplication(sys.argv)
    window = mainwindow.MainWindow()
    window.setup_log(furhat)

    window.addDefaultPhraseButtons(furhat)



    window.show()
    sys.exit(app.exec_())
