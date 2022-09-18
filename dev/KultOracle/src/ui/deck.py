from PyQt5 import QtWidgets

class DeckItem():

    def __init__(self, parent=None):
        self.__frontFaceImage = None
        self.__backFaceImage = None
        self.__title = ''
        self.__description = ''
        self.__showFrontFace=False
        
    def showFrontFace(self):
        return self.__showFrontFace

    def setShowFrontFace(self, bval):
        self.__showFrontFace=bval

    def setFrontFaceImage(self, frontFaceImage):
        self.__frontFaceImage=frontFaceImage
        
    def setBackFaceImage(self, backFaceImage):
        self.__backFaceImage=backFaceImage

    def setTitle(self, title):
        self.__title=title

    def setDescription(self, description):
        self.__title=description

    def getBackFaceImage(self):
        return self.__backFaceImage
    
    def getFrontFaceImage(self):
        return self.__frontFaceImage
       
    def getQGPBackFaceImage(self):
        return QtWidgets.QGraphicsPixmapItem(self.__backFaceImage)
    
    def getQGPFrontFaceImage(self):
        return QtWidgets.QGraphicsPixmapItem(self.__frontFaceImage)

    def getQGPVVisibleFaceImage(self):
        return self.getQGPFrontFaceImage() if self.showFrontFace() else self.getQGPBackFaceImage()


    def getTitle(self):
        return self.__title
        
    def getDescription(self):
        return self.__description

