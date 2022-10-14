'''
Created on Sep 11, 2022

@author: columbus
'''
from ui.Ui_descriptionwindow import Ui_DescriptionWindow
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtCore, QtWidgets
from resources import bitmaps_rc

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
        self.scrollArea.verticalScrollBar().setStyleSheet( 
                    """
         QScrollBar:vertical {
             border: 1px solid black;
             background: rgb(85, 0, 0);
             width: 22px;
             margin: 30px 0 30px 0;
         }
        
         QScrollBar::handle:vertical {
             background: rgb(83, 16, 18);
             min-height: 17px;
             border: 1px solid rgb(102, 45, 46);
         }
        
         QScrollBar::add-line:vertical {
             border: 1px solid rgb(102, 45, 46);
             background: rgb(85, 0, 0);
             width: 22px;
             height: 30px;
             subcontrol-position: bottom;
             subcontrol-origin: margin;
             
            image: url(:/data/skullud);
         }
        
         QScrollBar::sub-line:vertical {
             border: 1px solid rgb(102, 45, 46);
             background: rgb(85, 0, 0);
             width: 22px;
             height: 30px;
             subcontrol-position: top;
             subcontrol-origin: margin;
             image: url(:/data/skull);
         }
        
         QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
             border: 2px solid rgb(102, 45, 46);
             background: none;
             width: 15px;
         }
            """)
    
        
    def getLblDescription(self):
        return self.lblDescription
    