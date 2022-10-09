# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

from resources import bitmaps_rc

from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import pyqtSlot, QTimer,  QDir
from PyQt5.QtWidgets import QMainWindow,  QApplication

import random
import time
from ui.graphicsscene import GraphicsScene
from ui.Ui_mainwindow import Ui_MainWindow
from ui.Ui_customcursors import ManagerCursor
from ui.descriptionwindow import DescriptionWindow
from ui.deck import DeckItem
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

from PyQt5.Qt import QRect, Qt, QByteArray, QBuffer, QIODevice, QDataStream,\
    QFile
from PyQt5.QtGui import QIcon, QPixmap, QTransform, QPainter, QPen, QFont
from loader.pdfloader import PdfLoader
from ui.loader import LoaderWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(MainWindow, self).__init__(parent)
        #uic.loadUi('./ui/mainwindow.ui',self)
        #uic.loadUi('./ui/descriptionwindow.ui',self)
        self.setupUi(self)
        
        self.descriptionWindow = DescriptionWindow()
        
        
        self.setWindowIcon(QIcon(":/data/mainwindowicon"))
        
        self.frmCentralWidget.raise_()        
        #self.lblSilkScreen.hide()
        
        self.dwlblDescription=self.descriptionWindow.getLblDescription()
        self.lblSilkScreen.setText("")
        
        #only called to please the precompiler and remove unused warning
        bitmaps_rc.qt_resource_data=bitmaps_rc.qt_resource_data
        # ############################

        self._manager = ManagerCursor(self)
        movie = QtGui.QMovie(":/data/mousecursormain")
        self._manager.setMovie(movie)
        self._manager.setWidget(self)        
        self._manager.start()
               
        self.shuffleTimer = QTimer(self)
        self.shuffleTimer.setInterval(100) # interval in ms
        self.shuffleTimer.timeout.connect(self.updateCards)
        self.__sigilIdletTmeoutms=3000
        self.__sigilIdleTimeoutCurrentms=0
        
        self.installEventFilter(self)
        self.loaderWindow = LoaderWindow()
        
        self.initialiseResources()


    def initialiseResources(self):


        
        self.loadContentIntoDatabase()
        
        
        self.deckMajorArcana={}
        self.deckMinorArcana={}
        self.deckPrincipalities={}
        self.dctCardsInfo={}
        
        
        #self._populateDeck(":/data", "majorarcana_",  self.deckMajorArcana)
        #self._populateDeck(":/data", "minorarcana_",  self.deckMinorArcana)
        #self._populateDeck(":/data", "principalities_",  self.deckPrincipalities)
        self.populateDeckFromDb("MAJOR_ARCANA",  self.deckMajorArcana)
        self.populateDeckFromDb("MINOR_ARCANA",  self.deckMinorArcana)
        self.populateDeckFromDb("ALL",  self.deckPrincipalities)

        
        NAME, DESCRIPTION, SUIT, PRINCIPALITY, ARCANA = range(5)
        
        query = QSqlQuery("SELECT NAME, DESCRIPTION, SUIT, PRINCIPALITY, ARCANA FROM CARDS_DECK")

        while query.next():
            self.dctCardsInfo[query.value(NAME)]=(query.value(NAME),
                    query.value(DESCRIPTION), query.value(SUIT), query.value(PRINCIPALITY),
                        query.value(ARCANA))

        QSqlDatabase.removeDatabase(QSqlDatabase.database().connectionName())

        fdb=QFile('./kcdata')
        if fdb.exists():
            fdb.remove()

        self.lstPrevActiveDeck=list(self.deckMajorArcana.values())
        self.lstActiveDeck=list(self.deckPrincipalities.values())

        self.btnShuffle.setEnabled(False)
        self.btnArcanas.setEnabled(False)
        self.btnPrincipalities.setText('deck')
        self.lstChosenCards = [self.lstActiveDeck[i] for i in range(5)]

        for tc in self.lstChosenCards:
                tc.setShowFrontFace(True)

        self.initializeGraphicsViews()
        self.recreateItemsInViews()
        
        self.show()



    def retranslateUi(self, uiMainWindow):
        super(MainWindow, self).retranslateUi(uiMainWindow)
        _translate = QtCore.QCoreApplication.translate
        uiMainWindow.setWindowTitle(_translate("MainWindow", "KultOracle beta 0.1.0.0"))



    def loadContentIntoDatabase(self):
        
                
        workdir = "./" 
        deck_rules_filename='KULT Divinity Lost - Tarot Deck Rules.pdf'
        tarot_deck_filename='kult-tarot.pdf'
        
    
        pdfprocessor=PdfLoader(self.loaderWindow)
        
        pdfprocessor.processDocuments(workdir, deck_rules_filename, 
                                                     tarot_deck_filename)
    
    
    def populateDeckFromDb(self, arcana, deck):
    
        
        NAME, DESCRIPTION, SUIT, PRINCIPALITY, ARCANA, IMAGE, IMAGEBACK = range(7)
        
        query = QSqlQuery()
        prepstmnt = "SELECT NAME, DESCRIPTION, SUIT, PRINCIPALITY, ARCANA, IMAGE, IMAGEBACK " +\
                          "FROM CARDS_DECK WHERE ARCANA= ? ;"
    
        if not query.prepare(prepstmnt):
            print("query prep result: ",query.lastError().text())
        else:
            query.addBindValue(arcana)
            #print("query select exec res: ",query.exec())
            #print("query result: ",query.lastError().text())

        while query.next():
            
            tarotCard=DeckItem()
            tarotCard.setTitle(query.value(NAME))
            tarotCard.setDescription(query.value(DESCRIPTION))
            tarotCard.setSuit(query.value(SUIT))
            tarotCard.setPrincipality(query.value(PRINCIPALITY))
            tarotCard.setArcana(query.value(ARCANA))
    
            byteArray = QByteArray().fromHex(query.value(IMAGE))
            buffer =  QBuffer(byteArray)
            buffer.open(QIODevice.ReadOnly)
            inp = QDataStream (buffer)                        
            picdata = QPixmap()
            inp >> picdata                        
            tarotCard.setFrontFaceImage(picdata)
    
            byteArray = QByteArray().fromHex(query.value(IMAGEBACK))
            buffer =  QBuffer(byteArray)
            buffer.open(QIODevice.ReadOnly)
            inp = QDataStream (buffer)                        
            picdata = QPixmap()
            inp >> picdata
            tarotCard.setBackFaceImage(picdata)
    
            
            deck[query.value(NAME)]=tarotCard
            


    def _populateDeck(self,  path, term,  deck):
        
        directory = QDir(path)
        
        directory.setFilter(
        
            directory.filter() |
            QDir.NoDotAndDotDot |
            QDir.NoSymLinks
        )
        
        for entry in directory.entryInfoList():
            if term in entry.filePath() :
                if 'BackFaceImage' in entry.filePath() :
                    continue
                    
                tarotCard=DeckItem()
                tarotCard.setFrontFaceImage(QtGui.QPixmap(entry.filePath()))
                tarotCard.setBackFaceImage(QtGui.QPixmap(path+'/'+term+'BackFaceImage'))
                tarotCard.setTitle(entry.filePath()[entry.filePath().find('_')+1:-3])
                deck[tarotCard.getTitle()]=tarotCard
                
                #print(entry.filePath())
            if entry.isDir():
                self._populateDeck(term, entry.filePath(), deck)
    

    def updateCards(self):
        if self.__sigilIdleTimeoutCurrentms > self.__sigilIdletTmeoutms:
            self.shuffleTimer.stop()
            
            self.lblSilkScreen.setPixmap(self.lblSilkScreen.originalPixmap.copy())
            self.lblSilkScreen.set_opacity(0.7)
            
            self.frmCentralWidget.raise_()
            self.btnShuffle.raise_()
            
            self.__sigilIdleTimeoutCurrentms=0
            self.btnShuffle.setText("shuffle")
            self.btnShuffle.setEnabled(True)
            self.btnArcanas.setEnabled(True)
            self.btnPrincipalities.setEnabled(True)
            lstOfChosen = self.getRandomArcanaPick()
            self.lstChosenCards =[self.lstActiveDeck[lstOfChosen[i]] for i in range(5)]              
            self.showBackFacesInOrder()
            self._manager.stop()
            movie = QtGui.QMovie(":/data/mousecursormain")
            self._manager.setMovie(movie)    
            self._manager.start()
            #self.lblSilkScreen.hide()
        else:
            self.__sigilIdleTimeoutCurrentms += 100
            transform = QtGui.QTransform()
            #transform.translate(0, 0)
            #transform.scale(1.0, 1.0)
            
            transform.rotate(-(self.angle%365))
            self.angle+=3
            
            pixmap=self.lblSilkScreen.originalPixmap.copy()
            #self.lblSilkScreen.pixmap().copy()
            #pixmap=pixmap.transformed(transform)
            #self.lblSilkScreen.pixmap().transformed(transform)
            self.lblSilkScreen.setPixmap(pixmap.transformed(transform))
            self.lblSilkScreen.update()
            #pixmap=None
            self.showFrontFaces()


         
    def getRandomArcanaPick(self):
        rndResult=random.sample( range(len(self.lstActiveDeck)), 5)
        #print (rndResult)
        return rndResult
        
    def graphicsViewMousePressedEvent(self, caller, tarotCard,  event):
        tarotCard.setShowFrontFace(False if tarotCard.showFrontFace() else True)
        self.refreshCurrentViews()
        

    def graphicsViewDoubleClickEvent(self, caller, tarotCard,  event):
        if tarotCard.showFrontFace():
            self.dwlblDescription.setText(tarotCard.getDescription())
            self.descriptionWindow.setGeometry(QRect(self.geometry().left() + self.geometry().width(), 
                                                     self.geometry().top(), 360, self.geometry().height()))
            self.descriptionWindow.show()

    def closeEvent(self, event):
        self.descriptionWindow.close()
        event.accept()

    def eventFilter(self, source, event):
        #print ('event type:' + str(event.type()))
        if event.type() == QtCore.QEvent.HoverMove:
#            if event.buttons() == QtCore.Qt.NoButton:
#                pos = event.pos()
#                self.edit.setText('x: %d, y: %d' % (pos.x(), pos.y()))
            if 'time to invoke those spirits...' in self.btnShuffle.text():
                lstOfChosen = self.getRandomArcanaPick()
                self.lstChosenCards =[self.lstActiveDeck[lstOfChosen[i]] for i in range(5)]            
                self.__sigilIdleTimeoutCurrentms=0
        
        return QMainWindow.eventFilter(self, source, event)


#        if a0.buttons() == QtCore.Qt.RightButton:
#            a0.ignore()
#            return
#        if a0.buttons() == QtCore.Qt.MiddleButton:
#            # Drag the display
#            a0.accept()
#            if self.moveStartX != -1 and self.moveStartY != -1:
#                dx = self.moveStartX - a0.x()
#                dy = self.moveStartY - a0.y()
#                self.zoomTo(self.leftMargin + dx, self.topMargin + dy,
#                            self.leftMargin + self.chartWidth + dx,
#                            self.topMargin + self.chartHeight + dy)
#
#            self.moveStartX = a0.x()
#            self.moveStartY = a0.y()
#            return
#        if a0.modifiers() == QtCore.Qt.ControlModifier:
#            # Dragging a box
#            if not self.draggedBox:
#                self.draggedBoxStart = (a0.x(), a0.y())
#            self.draggedBoxCurrent = (a0.x(), a0.y())
#            self.update()
#            a0.accept()
#            return
#        x = a0.x()
#        f = self.frequencyAtPosition(x)
#        if x == -1:
#            a0.ignore()
#            return
#        a0.accept()
#        m = self.getActiveMarker()
#        if m is not None:
#            m.setFrequency(str(f))
#            m.frequencyInput.setText(str(f)) 


        
    @pyqtSlot()
    def on_btnShuffle_released(self):
        if self.shuffleTimer.isActive():            
            self.shuffleTimer.stop()
            self._manager.stop()
            movie = QtGui.QMovie(":/data/mousecursormain")
            self._manager.setMovie(movie)    
            self._manager.start()
        else:
            self.__sigilIdleTimeoutCurrentms=0
            self.btnShuffle.setText("time to invoke those spirits...")
            self.btnShuffle.setEnabled(False)
            self.btnArcanas.setEnabled(False)
            self.btnPrincipalities.setEnabled(False)
            self.lblSilkScreen.raise_()
            self.lblSilkScreen.set_opacity(0.7)
            #self.lblSilkScreen.show()
            self.angle=0
            self.showBackFaces()
            self.shuffleTimer.start()
            self._manager.stop()
            movie = QtGui.QMovie(":/data/mousecursorhand")
            self._manager.setMovie(movie)    
            self._manager.start()
            

    def showEvent(self, event):
        self.fitItemInViews()
    
    def resizeEvent(self, event):
        self.frmCentralWidget.resize(event.size())
        self.lblSilkScreen.resize(event.size())
        #print(event.size())
        self.lblSilkScreen.update()
        self.lblSilkScreen.originalPixmap=QtGui.QPixmap(":/data/gradients").scaledToHeight(event.size().height()*2)
        self.lblSilkScreen.setPixmap(self.lblSilkScreen.originalPixmap.copy())

        self.fitItemInViews()
        return QMainWindow.resizeEvent(self, event)
        #
        # self.lblSilkScreen.setGeometry(QRect(self.centralWidget.geometry().left(),
        #                                    self.centralWidget.geometry().top(),
        #                                    self.centralWidget.geometry().width(),
        #                                    self.centralWidget.geometry().height()))
        # self.lblSilkScreen.raise_()
        

    def initializeGraphicsViews(self):
        self.grvCardCenter.setScene(GraphicsScene(self))
        self.grvCardNorth.setScene(GraphicsScene(self))
        self.grvCardSouth.setScene(GraphicsScene(self))
        self.grvCardEast.setScene(GraphicsScene(self))
        self.grvCardWest.setScene(GraphicsScene(self))


    def refreshCurrentViews(self):
        self.recreateItemsInViews()
        self.fitItemInViews()

    def showFrontFaces(self):
        for tc in self.lstChosenCards:
                tc.setShowFrontFace(True)
                
        self.recreateItemsInViews()
        self.fitItemInViews()

    def showBackFacesInOrder(self):
        self.lstChosenCards[3].setShowFrontFace(False)        
        self.grvCardCenter.scene().clear()
        self.grvCardCenter.scene().tarotCard=self.lstChosenCards[3]
        self.grvCardCenter.scene().addItem(self.lstChosenCards[3].getQGPVVisibleFaceImage())
        QApplication.processEvents()
        time.sleep(.7)
        self.lstChosenCards[1].setShowFrontFace(False)        
        self.grvCardWest.scene().clear()
        self.grvCardWest.scene().tarotCard=self.lstChosenCards[1]
        self.grvCardWest.scene().addItem(self.lstChosenCards[1].getQGPVVisibleFaceImage())
        QApplication.processEvents()
        time.sleep(.7)
        self.lstChosenCards[0].setShowFrontFace(False)        
        self.grvCardNorth.scene().clear()
        self.grvCardNorth.scene().tarotCard=self.lstChosenCards[0]
        self.grvCardNorth.scene().addItem(self.lstChosenCards[0].getQGPVVisibleFaceImage())
        QApplication.processEvents()
        time.sleep(.7)
        self.lstChosenCards[2].setShowFrontFace(False)        
        self.grvCardEast.scene().clear()
        self.grvCardEast.scene().tarotCard=self.lstChosenCards[2] 
        self.grvCardEast.scene().addItem(self.lstChosenCards[2].getQGPVVisibleFaceImage()) 
        QApplication.processEvents()
        time.sleep(.7)
        self.lstChosenCards[4].setShowFrontFace(False)        
        self.grvCardSouth.scene().clear()
        self.grvCardSouth.scene().tarotCard=self.lstChosenCards[4]
        self.grvCardSouth.scene().addItem(self.lstChosenCards[4].getQGPVVisibleFaceImage())
        QApplication.processEvents()
        time.sleep(.7)
                
        self.fitItemInViews()

    def showBackFaces(self):
        for tc in self.lstChosenCards:
                tc.setShowFrontFace(False)

        self.recreateItemsInViews()
        self.fitItemInViews()

    def recreateItemsInViews(self):
        lstQGPFItems=[self.lstChosenCards[i].getQGPVVisibleFaceImage() for i in range(5)]
        self.grvCardCenter.scene().clear()
        self.grvCardNorth.scene().clear()
        self.grvCardSouth.scene().clear()
        self.grvCardEast.scene().clear()
        self.grvCardWest.scene().clear()

        self.grvCardCenter.scene().tarotCard=self.lstChosenCards[3]
        self.grvCardWest.scene().tarotCard=self.lstChosenCards[1]
        self.grvCardNorth.scene().tarotCard=self.lstChosenCards[0]
        self.grvCardEast.scene().tarotCard=self.lstChosenCards[2]
        self.grvCardSouth.scene().tarotCard=self.lstChosenCards[4]

        self.grvCardCenter.scene().addItem(lstQGPFItems[3])
        self.grvCardWest.scene().addItem(lstQGPFItems[1])
        self.grvCardNorth.scene().addItem(lstQGPFItems[0])
        self.grvCardEast.scene().addItem(lstQGPFItems[2]) 
        self.grvCardSouth.scene().addItem(lstQGPFItems[4])
        
    def fitItemInViews (self):        
        lstQGPFItems=[self.lstChosenCards[i].getQGPVVisibleFaceImage() for i in range(5)]
        self.grvCardCenter.centerOn(lstQGPFItems[3])
        self.grvCardNorth.centerOn(lstQGPFItems[0])
        self.grvCardSouth.centerOn(lstQGPFItems[4])
        self.grvCardEast.centerOn(lstQGPFItems[2])
        self.grvCardWest.centerOn(lstQGPFItems[1])
 
        self.grvCardCenter.fitInView(lstQGPFItems[3], QtCore.Qt.KeepAspectRatio)
        self.grvCardNorth.fitInView(lstQGPFItems[0], QtCore.Qt.KeepAspectRatio)
        self.grvCardSouth.fitInView(lstQGPFItems[4], QtCore.Qt.KeepAspectRatio)
        self.grvCardEast.fitInView(lstQGPFItems[2], QtCore.Qt.KeepAspectRatio)
        self.grvCardWest.fitInView(lstQGPFItems[1], QtCore.Qt.KeepAspectRatio)
    
    @pyqtSlot()
    def on_btnPrincipalities_released(self):
        """
        Slot documentation goes here.
        """
        if 'principalities' in self.btnPrincipalities.text():
            self.btnShuffle.setEnabled(False)
            self.btnArcanas.setEnabled(False)
            self.btnPrincipalities.setText('deck')
            self.lstPrevActiveDeck = self.lstActiveDeck
            self.lstActiveDeck = list(self.deckPrincipalities.values())
            self.lstChosenCards = [self.lstActiveDeck[i] for i in range(5)]
            self.showFrontFaces()
        else:
            self.btnShuffle.setEnabled(True)
            self.btnArcanas.setEnabled(True)
            self.btnPrincipalities.setText('principalities')
            self.lstActiveDeck = self.lstPrevActiveDeck
            self.lstChosenCards = [self.lstActiveDeck[i] for i in range(5)]
            for tarotCard in self.lstActiveDeck:
                tarotCard.setShowFrontFace(False)
            self.refreshCurrentViews()
            

 
    @pyqtSlot()
    def on_btnArcanas_released(self):
        """
        Slot documentation goes here.
        """
        if 'major arcana' in self.btnArcanas.text():
            self.btnArcanas.setText('minor arcana')
            self.lstPrevActiveDeck = self.lstActiveDeck
            self.lstActiveDeck = list(self.deckMajorArcana.values())
            lstOfChosen = self.getRandomArcanaPick()
            self.lstChosenCards =[self.lstActiveDeck[lstOfChosen[i]] for i in range(5)]
        else:
            self.btnArcanas.setText('major arcana')
            self.lstPrevActiveDeck = self.lstActiveDeck
            self.lstActiveDeck = list(self.deckMinorArcana.values())
            lstOfChosen = self.getRandomArcanaPick()
            self.lstChosenCards =[self.lstActiveDeck[lstOfChosen[i]] for i in range(5)]

        self.btnShuffle.setEnabled(True)
        
        for tarotCard in self.lstActiveDeck:
            tarotCard.setShowFrontFace(False)
            
        self.refreshCurrentViews()

