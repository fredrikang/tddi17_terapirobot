# This Python file uses the following encoding: utf-8
import sys
import xyz
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtCore import QFile, QIODevice

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = QMainWindow()
    window = xyz.Ui_MainWindow()
    window.setupUi(w)
    window.retranslateUi(w)
    w.show()
    sys.exit(app.exec_())
