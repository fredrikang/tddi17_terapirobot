# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PySide2 import QtCore, QtGui, QtWidgets
import PySide2
import PySide2.QtWidgets
from PySide2.QtWidgets import QMainWindow
import time
import sys
from defaultphraseswidget import DefaultPhrasesWidget
from gestureswidget import GesturesWidget
from statebuttonswidget import StateButtonsWidget
from furhatinterface import FurhatInterface
from furhatvideo import FurhatVideoAudioWidget
from furhatspeech import FurhatSpeechWidget

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1042)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMaximumSize(QtCore.QSize(1920, 1210))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QtCore.QSize(0, 0))
        self.frame.setMaximumSize(QtCore.QSize(16777215, 1000))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        



        self.fVideoWindow = FurhatVideoAudioWidget()
        self.verticalLayout_2.addWidget(self.fVideoWindow, 0, QtCore.Qt.AlignTop)
       


        self.listView = QtWidgets.QListView(self.frame)
        self.listView.setMinimumSize(QtCore.QSize(0, 50))
        self.listView.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.listView.setObjectName("listView")
        self.verticalLayout_2.addWidget(self.listView)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.textEdit = QtWidgets.QTextEdit(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy)
        self.textEdit.setMinimumSize(QtCore.QSize(0, 0))
        self.textEdit.setMaximumSize(QtCore.QSize(16777215, 60))
        self.textEdit.setObjectName("textEdit")
        self.horizontalLayout_2.addWidget(self.textEdit)
        self.pushButtonSend = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonSend.sizePolicy().hasHeightForWidth())
        self.pushButtonSend.setSizePolicy(sizePolicy)
        self.pushButtonSend.setMaximumSize(QtCore.QSize(16777215, 60))
        self.pushButtonSend.setObjectName("pushButtonSend")
        self.horizontalLayout_2.addWidget(self.pushButtonSend)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1, QtCore.Qt.AlignLeft)
        self.frame_3 = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.gridLayout.addWidget(self.frame_3, 0, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1920, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)



    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "FurhatController"))
        self.pushButtonSend.setText(_translate("MainWindow", "Send"))

    def addDefaultPhraseButtons(self, furhat):
        ## Default Buttons ##
        defaultPhrasesWidget = DefaultPhrasesWidget(furhat)
        defaultPhrasesFile = open('defaultphrases.txt', 'r')
        defaultPhrases = defaultPhrasesFile.readlines()
        defaultPhrasesWidget.addPhrases(defaultPhrases)
        self.verticalLayout_4.addWidget(defaultPhrasesWidget)

    def addGestureButtons(self, furhat):
        gesturesWidget = GesturesWidget(furhat)
        gesturesFile = open('gestures.txt', 'r')
        gestures = gesturesFile.readlines()
        gesturesWidget.addGestures(gestures)
        self.verticalLayout_4.addWidget(gesturesWidget)

    def addStates(self, furhat):
        stateWidget = StateButtonsWidget(furhat)
        defaultStatesFile = open('states.txt', 'r')
        defaultStates = defaultStatesFile.readlines()
        stateWidget.addStates(defaultStates)
        self.verticalLayout_4.addWidget(stateWidget)



    def addChangeModeButton(self, furhat):
        self.changeModeButton = QtWidgets.QPushButton("Change to Controlled Mode")
        self.changeModeButton.clicked.connect(lambda: furhat.change_mode())
        self.verticalLayout_4.addWidget(self.changeModeButton)
        furhat.subscribe("CancelAutonomousState", self.setChangeModeButtonTextAuto)
        furhat.subscribe("CancelControlledDialogState", self.setChangeModeButtonTextControlled)

    def setChangeModeButtonTextAuto(self,event):
        self.changeModeButton.setText("Change to Autonomous Mode")
    
    def setChangeModeButtonTextControlled(self, event):
        self.changeModeButton.setText("Change to Controlled Mode")

    def setup_log(self, furhat):
        print("setup log")
        furhat.subscribe("furhatos.event.senses.speech.rec", self.append_log_client)
        furhat.subscribe("furhatos.event.actions.ActionSpeech", self.append_log_furhat_skill)
        furhat.subscribe("furhatos.event.senses.SenseNLUIntent", self.append_log_client)
        
        self.listView_model = QtGui.QStandardItemModel()
        self.listView.setModel(self.listView_model)

    def append_log_client(self, event):
        item = QtGui.QStandardItem("CLIENT: " + event.text)
        self.listView_model.appendRow(item)
        self.listView.scrollToBottom()

    def append_log_furhat_skill(self, event):
        while True:
            i = event.text.find('<')
            if i == -1: break
            j = event.text.find('>', i + 1)
            if j == -1: break
            event.text = event.text.replace(event.text[i:j + 1], '')
            
        item = QtGui.QStandardItem("FURHAT: " + event.text)
        self.listView_model.appendRow(item)
        self.listView.scrollToBottom()

    def addVideoStream(self, host: str):
        self.fVideoWindow.start_videostream(host)
        self.fVideoWindow.start_audiostream(host)

    def addChangeStateButtons(self, furhat):
        self.pushButtonChangeMode = QtWidgets.QPushButton(self.frame)
        self.pushButtonChangeMode.setText(_translate("MainWindow", "Change Mode"))
    
    def setupSendButton(self, furhat):
        self.pushButtonSend.clicked.connect(lambda state = False: self.speak(furhat))

    
    def speak(self, furhat):
        furhat.speak(self.textEdit.toPlainText())
        self.textEdit.setPlainText("")

    def setupSpeech(self, furhat):
        speech = FurhatSpeechWidget(furhat, self.textEdit)
        self.verticalLayout_2.addWidget(speech)
    
    

        

        
        