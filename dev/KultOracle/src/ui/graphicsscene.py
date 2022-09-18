#from PyQt5 import QtCore
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QGraphicsScene, QApplication
#from PyQt5.QtGui import QPen,  QBrush

class GraphicsScene(QGraphicsScene):
    def __init__(self, parent=None):
        QGraphicsScene.__init__(self, parent)
        #self.setSceneRect(-100, -100, 200, 200)
        self.opt = ""
        self.tarotCard=None
        self.message=""
        
    def mousePressEvent(self, event):
        self.last = "Click"
    
    def mouseReleaseEvent(self, event):
    
        if self.last == "Click":
            self.singleClickEvent=event
            QTimer.singleShot(QApplication.instance().doubleClickInterval(),
                              self.performSingleClickAction)
        else:
            # Perform double click action.
            self.message = "Double Click"
            self.update()
   
    def mouseDoubleClickEvent(self, event):
        self.parent().graphicsViewDoubleClickEvent(self, self.tarotCard, event)
        self.last = "Double Click"
     
    def performSingleClickAction(self):
        if self.last == "Click":
            self.parent().graphicsViewMousePressedEvent(self, self.tarotCard, self.singleClickEvent)
            self.singleClickEvent=None
            self.message = "Click"
            self.update()

