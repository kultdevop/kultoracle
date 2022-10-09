'''
Created on Oct 2, 2022

@author: columbus
'''


from itertools import islice
import re
import sys
from time import sleep

from PIL.Image import frombytes
from PIL.ImageQt import ImageQt
from PyQt5.Qt import QByteArray, \
    QBuffer, QIODevice, QDataStream
from PyQt5.QtGui import QPixmap
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtWidgets import QApplication
import fitz


# Create window
class PdfLoader(object):
    '''
    classdocs
    '''


    def __init__(self, _loaderWindow):
        '''
        Constructor
        '''
        self.loaderWindow = _loaderWindow



    def populateDeckContent(self, regex,fulltext,key,suit,principality,arcana,dct):
        if match := re.search(regex, fulltext, re.IGNORECASE):        
            dct[key]=dict(DESCRIPTION=str(match.group(1)),SUIT = suit, PRINCIPALITY=principality, 
                                                                        ARCANA=arcana, IMAGE=None, IMAGEBACK=None)
            #print(str(dct[key]))
            
    
    def processArcanas(self, fulltext, arcana, dct, startid=0):
        i=startid
        
        regex = r"(?sm)(?:^"+str(i)+"\.\s(\w+(?:-\w*)*)(.*$.*)^"+str(i+1)+"\. )|(?:^"+str(i)+"\.\s(\w+(?:-\w*)*)(.*$.*)\Z)"
        while match := re.search(regex, fulltext, re.IGNORECASE):        
            
            name=match.group(3) if match.group(1)is None else match.group(1)
            body=match.group(4) if match.group(2)is None else match.group(2)
            key=str(name+str(i).zfill(3)).upper()
            dct[key]=body
            #print(dct[key])
            i+=1
        
            regex = r"(?sm)(?:^"+str(i)+"\.\s(\w+(?:-\w*)*)(.*$.*)^"+str(i+1)+"\. )|(?:^"+str(i)+"\.\s(\w+(?:-\w*)*)(.*$.*)\Z)"
        
        dcttmp={}
        
        for key in dct.keys():
            item = dct[key]
            
            if 'demiurge' in key.lower():
                dcttmp[key.replace('DEMIURGE', 'DEMIURGOS')]=item
            else:
                dcttmp[key]=dct[key]
        
        dct.clear()
        
        for key in dcttmp.keys():
            dct[key]=dcttmp[key]
        
        
        
    def loadMajorArcanaInfo(self, buf, dct):
        arcana='MAJOR_ARCANA'
        
        regex = '(?sm)^The\s{1,5}Death\s{1,5}Angels\s{1,5}(.*)^Guide\s{1,5}to\s{1,5}Using'
        suit='DEATH ANGEL'
        
        if match := re.search(regex, buf, re.IGNORECASE):        
            
            subtext=str(match.group(1))
            regex=r'(?i)KHLD\s{1,5}[\W]+(\w+(?:-\w*)*)'
            
            for key in dct.keys():
                if match := re.search(regex.replace('KHLD', key[:-3]), subtext, re.IGNORECASE):
                    principality=match.group(1)
                    dct[key]=dict(DESCRIPTION=dct[key] ,SUIT = suit, PRINCIPALITY=principality, ARCANA=arcana, IMAGE=None, IMAGEBACK=None)
            
        
        regex = '(?sm)^The\s{1,5}Archons\s{1,5}(.*)^The\s{1,5}Death'
        suit='ARCHON'
        
        if match := re.search(regex, buf, re.IGNORECASE):        
            
            subtext=str(match.group(1))
            regex=r'(?i)KHLD\s{1,5}[\W]+(\w+(?:-\w*)*)'
            
            for key in dct.keys():
                if match := re.search(regex.replace('KHLD', key[:-3]), subtext, re.IGNORECASE):
                    principality=match.group(1)
                    dct[key]=dict(DESCRIPTION=dct[key] ,SUIT = suit, PRINCIPALITY=principality, ARCANA=arcana, IMAGE=None, IMAGEBACK=None)
            
        suit='CREATOR'
        
        principality='METROPOLIS'
        key='ANTHROPOS000'
        dct[key]=dict(DESCRIPTION=dct[key] ,SUIT = suit, PRINCIPALITY=principality, ARCANA=arcana, IMAGE=None, IMAGEBACK=None)
        
        principality='ELYSIUM'
        key='DEMIURGOS001'
        dct[key]=dict(DESCRIPTION=dct[key] ,SUIT = suit, PRINCIPALITY=principality, ARCANA=arcana, IMAGE=None, IMAGEBACK=None)
        
        principality='INFERNO'
        key='ASTAROTH002'
        dct[key]=dict(DESCRIPTION=dct[key] ,SUIT = suit, PRINCIPALITY=principality, ARCANA=arcana, IMAGE=None, IMAGEBACK=None)
        
    
    def loadMinorArcana(self, buf, dct):
        arcana='MINOR_ARCANA'
        suits=(('SKULL','DEATH'),('ROSE','PASSION'),('HOURGLASS','LABYRINTH'),('CRESCENT','MOON'),('EYE','ELYSIUM'))
        regex = r'(?sm)(^1\. .*?)((?=^1\. )|\Z)'
        regexextractsuitdesc = r'(?sm)(SUITPLH\w(?:-\w*)*$.*?\.[\n])'
        suit='SKULLS'
        
        for match in re.findall(regex, buf, re.IGNORECASE):        
            
            subtext=match[0]
            currsuit=''
            suitdesc=''
            for suit in suits:
                if match := re.search(regexextractsuitdesc.replace('SUITPLH', suit[0]), 
                                      subtext, re.IGNORECASE):
                    suitdesc=match.group(1)
                    currsuit=suit[0]
                    currprincipality=suit[1]
                    subtext = subtext.replace(suitdesc,'')
            
            regex_card='(?sm)(^(\d+)\. (\w+(?:-\w*)*).*?)((?=^\d+\. )|\Z)'
            
            for match_card in re.findall(regex_card, subtext, re.IGNORECASE):
                dct[match_card[2] + match_card[1].zfill(3)]=dict(DESCRIPTION=suitdesc + '\n\n' +match_card[0] ,
                                SUIT = currsuit, PRINCIPALITY=currprincipality, ARCANA=arcana, IMAGE=None, IMAGEBACK=None)
            
    
    def sanitize_text(self,text):
        
        t = re.sub(r'(?m)(?:^\d+\n){2,}', '', text, count=0, flags=0)
        t = re.sub(r'(\w+)-\n', r'\n\1', t, count=0, flags=0)
        return t
    
    
    def getpdftext(self, workdir, filename):
        doc = fitz.Document(workdir + filename )
        pages = [ doc[ i ] for i in range( doc.page_count ) ]
        fulltext_buffer=''
        
        
        for page in pages:
            
            t= page.get_textpage()
            
            for block in t.extractBLOCKS():
                fulltext_buffer+=str(block[4])
    
        return self.sanitize_text(fulltext_buffer)


    def populateImageData(self, deckcontentdct, workdir, deck_rules_filename, backimagename):
            
        doc = fitz.Document(workdir+deck_rules_filename)
        toc = doc.get_toc(False)
        
        for toc_page in toc:
            for key in  islice(deckcontentdct.keys(), 5, sys.maxsize):
                if key[:-3] in toc_page[1].upper():
                    for img in doc.get_page_images(toc_page[2]-1):
                        xref = img[0]
                        image = doc.extract_image(xref)
        
                        self.loaderWindow.stepCompleted(0.3, \
                            f"processing visual art {key} width = {image['width']} height = {image['height']}")

                        #print(f"\nwidth = {image['width']} height = {image['height']}")
                        
                        if image["width"]==390 and image["height"] == 686:
                            pix = fitz.Pixmap(doc, xref)
                            pilimg = frombytes('RGB', [pix.width, pix.height], pix.samples,'raw')
                            qimage = ImageQt( pilimg).copy()
    
                            #label = QLabel(self.w)
                            
                            pixmap = QPixmap.fromImage(qimage)
                                                    
                            byteArray = QByteArray()
                            buffer =  QBuffer(byteArray)
                            buffer.open(QIODevice.WriteOnly)
                            
                            out = QDataStream (buffer)
                            out << pixmap
    
                            deckcontentdct[key]['IMAGE'] = byteArray.toHex()

    
                            byteArray = QByteArray().fromHex(deckcontentdct[key]['IMAGE'])
                            buffer =  QBuffer(byteArray)
                            buffer.open(QIODevice.ReadOnly)
                            inp = QDataStream (buffer)                        
                            picdata = QPixmap()
                            inp >> picdata                        
                            
                            #self.w.resize(picdata.width(), picdata.height())
                            
                            #label.setPixmap(picdata)
                            # Draw window
                            #self.w.show()
                            # Create widget
                            #self.app.exec_()
    
                            #label.deleteLater()


        zoom_x = 2  # horizontal zoom
        zoom_y = 2  # vertical zoom
        mat = fitz.Matrix(zoom_x, zoom_y)  # zoom factor 2 in each dimension

        pix = doc[73].get_pixmap(matrix=mat)
        #print("page: ", doc[73].get_label())
        pilimg = frombytes('RGB', [pix.width, pix.height], pix.samples,'raw')
        qimage = ImageQt( pilimg).copy()
        #label = QLabel(self.w)
        
        pixmap = QPixmap.fromImage(qimage)
        
        byteArray = QByteArray()
        buffer =  QBuffer(byteArray)
        buffer.open(QIODevice.WriteOnly)
        
        out = QDataStream (buffer)
        out << pixmap
        principalitiesbackimage = byteArray.toHex()

        principalitiesscreen = ('FRONT COVER003', 'ARCHONS002', 'DEATH ANGELS004', 'KULT GUIDE URL005', 'SUITS001')
        
        for i in range(4):
            pix = doc[i].get_pixmap(matrix=mat)
            #print("page: ", doc[i].get_label())
            pilimg = frombytes('RGB', [pix.width, pix.height], pix.samples,'raw')
            qimage = ImageQt( pilimg).copy()
            #label = QLabel(self.w)
            self.loaderWindow.stepCompleted(0.2, \
                f"{key} width = {pix.width} height = {pix.height}")
            
            pixmap = QPixmap.fromImage(qimage)
            
            byteArray = QByteArray()
            buffer =  QBuffer(byteArray)
            buffer.open(QIODevice.WriteOnly)
            
            out = QDataStream (buffer)
            out << pixmap
            deckcontentdct[principalitiesscreen[i]]['IMAGE'] = byteArray.toHex()
            deckcontentdct[principalitiesscreen[i]]['IMAGEBACK'] = principalitiesbackimage
        
        
        deckcontentdct[principalitiesscreen[4]]['IMAGE'] = deckcontentdct['METROPOLIS001']['IMAGE']
        deckcontentdct[principalitiesscreen[4]]['IMAGEBACK'] = principalitiesbackimage
        

        #Add the back image to the full deck
        for key in islice(deckcontentdct.keys(), 5, sys.maxsize):
            deckcontentdct[key]["IMAGEBACK"]=deckcontentdct[backimagename]["IMAGE"]


    def processDocuments(self, 
                        workdir,                        
                        deck_rules_filename,
                        tarot_deck_filename):
        
        
        self.loaderWindow.resetProgress("standby, the gathering is about to commence ...")
        sleep(2)
        self.loaderWindow.show()
        QApplication.processEvents()


        
        fulltext_major_arcana_buffer = ''
        fulltext_minor_arcana_buffer = ''
        
        deckcontentdct={}
    
        filename=deck_rules_filename    
        fulltext_buffer = self.getpdftext( workdir, filename )
            
        filename=tarot_deck_filename    
        fulltext_tarot_deck = self.getpdftext( workdir, filename )
    
        
        self.loaderWindow.stepCompleted(5, "loading front cover")
    
        #FRONT COVER
        regex = r"(?s)(Basic\s{1,5}Guidelines.*)Example\s{1,5}reading"
        self.populateDeckContent(regex,fulltext_buffer,'FRONT COVER003','COVER','ALL','ALL',deckcontentdct)

        self.loaderWindow.stepCompleted(5, "loading archons background data")
    
        #'ARCHONS'
        regex = r"(?sm)Reading\s{1,5}Templates\s{1,5}The\s{1,5}Major\s{1,5}Arcana(.*)^0. "
        self.populateDeckContent(regex,fulltext_buffer,'ARCHONS002','COVER','ALL','ALL',deckcontentdct)
            
    
        self.loaderWindow.stepCompleted(5, "adding death angels")
    
        #'DEATH ANGELS'
        regex = r"(?sm)Reading\s{1,5}Templates\s{1,5}The\s{1,5}Major\s{1,5}Arcana(.*)^0. "
        self.populateDeckContent(regex,fulltext_buffer,'DEATH ANGELS004','COVER','ALL','ALL',deckcontentdct)
            
            
        self.loaderWindow.stepCompleted(5, "getting suits")
    
        #'SUITS'
        regex = r"(?sm)^The\s{1,5}Minor\s{1,5}Arcana\s{1,5}(The\s{1,5}Minor\s{1,5}Arcana.*)^Skulls"
        self.populateDeckContent(regex, fulltext_buffer, 'SUITS001','COVER','ALL','ALL', deckcontentdct)
        
    
        self.loaderWindow.stepCompleted(5, "reading kult guide")
        
        #'KULT GUIDE URL'
        deckcontentdct['KULT GUIDE URL005']='Guide to Using\nthe Tarot Deck\nhttps://kultdivinitylost.com/tarot'
        deckcontentdct['KULT GUIDE URL005']=dict( DESCRIPTION=deckcontentdct['KULT GUIDE URL005'], SUIT='COVER',
                            PRINCIPALITY='ALL',ARCANA='ALL',IMAGE=None, IMAGEBACK=None)
        
    
        self.loaderWindow.stepCompleted(5, "loading major arcanas")
        
        #'The Major Arcana'
        regex=r"(?sm)(^0\.\s{1,5}\w+(?:-\w*)*$.*)\d{1,3}\s{1,5}^The\s{1,5}Major\s{1,5}Arcana\s{1,5}"
        if match := re.search(regex, fulltext_buffer, re.IGNORECASE):
            fulltext_major_arcana_buffer=match.group(1)    
            self.processArcanas(fulltext_major_arcana_buffer, 'MAJOR_ARCANA', deckcontentdct)    
            self.loadMajorArcanaInfo(fulltext_tarot_deck, deckcontentdct)
        
        
        self.loaderWindow.stepCompleted(5, "getting minor arcanas")
        
        #'The Minor Arcana'
        regex=r"(?sm)(^1\.\s{1,5}\w+(?:-\w*)*$.*\.)(?:\s{1,5}^\d{1,3}\s{1,5}^The\s{1,5}Minor\s{1,5}Arcana\s{1,5})"
        if match := re.search(regex, fulltext_buffer.replace(fulltext_major_arcana_buffer, ""), re.IGNORECASE):
            fulltext_minor_arcana_buffer=match.group(1)    
            #processArcanas(fulltext_minor_arcana_buffer, 'MINOR_ARCANA',deckcontentdct, 1)
            self.loadMinorArcana(fulltext_minor_arcana_buffer, deckcontentdct)
    
        self.loaderWindow.stepCompleted(5, "processing visual art")
    
        self.populateImageData( deckcontentdct, workdir, tarot_deck_filename,'METROPOLIS001' )
        

        self.loaderWindow.stepCompleted(5, "projecting onto database")
    
        query = QSqlQuery()
        
        prepstmnt= "INSERT INTO CARDS_DECK ( NAME, DESCRIPTION, SUIT, PRINCIPALITY, ARCANA, IMAGE, IMAGEBACK) " + \
                        "VALUES ( ?,?,?,?,?,?,? )"

    
        for key in deckcontentdct:
            if not query.prepare(prepstmnt):
                print("query prep result: ",query.lastError().text())
            else:
                query.addBindValue(key)
                query.addBindValue(deckcontentdct[key]["DESCRIPTION"])
                query.addBindValue(deckcontentdct[key]["SUIT"])
                query.addBindValue(deckcontentdct[key]["PRINCIPALITY"])
                query.addBindValue(deckcontentdct[key]["ARCANA"])
                query.addBindValue(deckcontentdct[key]["IMAGE"])
                query.addBindValue(deckcontentdct[key]["IMAGEBACK"])

                self.loaderWindow.stepCompleted(0.3, f"{key} {deckcontentdct[key]['SUIT']}")
    
            if not query.exec():    
                print("query result: ",query.lastError().text())
            
        
        self.loaderWindow.stepCompleted(10, "loading complete!, initialising Kult Oracle interface...")
        QApplication.processEvents()
        sleep(5)
    
        self.loaderWindow.hide()
    
