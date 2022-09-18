'''
Created on Sep 11, 2022

@author: columbus
'''
from ui.Ui_descriptionwindow import Ui_DescriptionWindow
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtCore

class DescriptionWindow(QMainWindow, Ui_DescriptionWindow):
    '''
    classdocs
    '''


    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(DescriptionWindow, self).__init__(parent)
        #uic.loadUi('./ui/mainwindow.ui',self)
        #uic.loadUi('./ui/descriptionwindow.ui',self)
        
        self.setupUi(self)
        self.lblDescription.setAlignment(QtCore.Qt.AlignCenter)
        
    def getLblDescription(self):
        return self.lblDescription