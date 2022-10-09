'''
Created on Oct 8, 2022

@author: columbus
'''
from ui.Ui_loader import Ui_LoaderWindow
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import QtCore
from PyQt5.Qt import QTimer, Qt, pyqtSlot
from time import sleep
from PyQt5.QtGui import QIcon

class LoaderWindow(QMainWindow, Ui_LoaderWindow):
    '''
    classdocs
    '''


    def __init__(self, parent=None):

        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(LoaderWindow, self).__init__(parent)
        #uic.loadUi('./ui/mainwindow.ui',self)
        #uic.loadUi('./ui/descriptionwindow.ui',self)
        self.setupUi(self)
        # this will hide the title bar
        self.setWindowFlag(Qt.FramelessWindowHint)

        
        self.__currprogress = 0
        self.__currdescription = ''
        self.setWindowIcon(QIcon(":/data/mainwindowicon"))
        
        #self.updateTimer = QTimer(self)
        #self.updateTimer.setInterval(10) # interval in ms
        #self.updateTimer.timeout.connect(self.updateProgressFeedback)
        
        self.center()
        
    
    def center(self):
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

        
    def stepCompleted(self, percentage, taskdescription):
        QApplication.processEvents()
        newvalue = 100 if self.__currprogress + percentage > 100 else self.__currprogress + percentage
        self.__currprogress = newvalue
        self.__currdescription = taskdescription
        QApplication.processEvents()
        self.updateProgressFeedback()
        self.update()
        #if percentage > 4:
        #    sleep(1)
        
    def resetProgress(self, taskdescription):
        self.__currprogress = 0
        self.__currdescription = taskdescription
        #self.updateTimer.start()
        self.updateProgressFeedback()
        self.update()

        
        
    def updateProgressFeedback(self):
        _translate = QtCore.QCoreApplication.translate
        self.lblStatus.setText(_translate("LoaderWindow",self.__currdescription))
        self.pbPdfLoader.setProperty("value",self.__currprogress)
        self.update()
    