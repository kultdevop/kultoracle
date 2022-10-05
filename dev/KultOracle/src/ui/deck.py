from PyQt5 import QtWidgets

class DeckItem():

    def __init__(self, parent=None):
        self.__frontFaceImage = None
        self.__backFaceImage = None
        self.__title = ''
        self.__description = ''
        self.__suit = ''
        self.__principality = ''
        self.__arcana = ''
        self.__showFrontFace=False
        
    
    def setTitle(self, title):
        self.__title=title

    def getTitle(self):
        return self.__title

    def setDescription(self, description):
        self.__description=description
        
    def getDescription(self):
        return self.__description

    def setSuit(self, suit):
        self.__suit=suit
        
    def getSuit(self):
        return self.__suit

    def setPrincipality(self, principality):
        self.__principality=principality
        
    def getPrincipality(self):
        return self.__principality
    
    def setArcana(self, arcana):
        self.__principality=arcana
        
    def getArcana(self):
        return self.__arcana
    
    def showFrontFace(self):
        return self.__showFrontFace

    def setShowFrontFace(self, bval):
        self.__showFrontFace=bval

    def setFrontFaceImage(self, frontFaceImage):
        self.__frontFaceImage=frontFaceImage
    
    def getFrontFaceImage(self):
        return self.__frontFaceImage
            
    def setBackFaceImage(self, backFaceImage):
        self.__backFaceImage=backFaceImage
    
    def getBackFaceImage(self):
        return self.__backFaceImage
   
    def getQGPBackFaceImage(self):
        return QtWidgets.QGraphicsPixmapItem(self.__backFaceImage)
    
    def getQGPFrontFaceImage(self):
        return QtWidgets.QGraphicsPixmapItem(self.__frontFaceImage)

    def getQGPVVisibleFaceImage(self):
        return self.getQGPFrontFaceImage() if self.showFrontFace() else self.getQGPBackFaceImage()

