'''
Created on Sep 13, 2022

@author: columbus
'''
from PyQt5.Qt import Qt
from PyQt5.QtGui import QPainter, QPen, QFont
from PyQt5.QtWidgets import QLabel, QGraphicsOpacityEffect
from PyQt5 import QtGui


class SilkScreenLabel(QLabel):
    '''
    classdocs
    '''


    def __init__(self, parent=None):
        '''
        Constructor
        '''
        super(SilkScreenLabel, self).__init__(parent)
        #uic.loadUi('./ui/mainwindow.ui',self)
        #uic.loadUi('./ui/descriptionwindow.ui',self)
        
        self.setAlignment(Qt.AlignCenter)
        
        self.set_opacity(0.5)
           
        self.originalPixmap=QtGui.QPixmap(":/data/gradients").scaledToHeight(int(self.height()*1.3))
        
        self.setPixmap(self.originalPixmap.copy())
 
        
        #self.delta = 45

    # def paintEvent(self, event):
        
        # painter = QPainter(self)
        # painter.setPen(QPen(Qt.blue, 1, Qt.DashLine))
        # painter.drawRect(0, 0, 500, 500)
        #
        #
        # painter.rotate(self.delta)
        #
        # self.delta += 45
        #
        # if self.delta == 365:
        #     self.delta= 0
        #
        #
        # painter.setFont(QFont("Helvetica", 10))
        # painter.setPen(QPen(Qt.black, 1))
        # painter.drawText(200, 200, "QTransform")
        # self.update()

    def set_opacity(self,level):
                # creating a opacity effect
        self.opacity_effect = QGraphicsOpacityEffect()
        # setting opacity level
        self.opacity_effect.setOpacity(level)
        # adding opacity effect to the label
        self.setGraphicsEffect(self.opacity_effect)
