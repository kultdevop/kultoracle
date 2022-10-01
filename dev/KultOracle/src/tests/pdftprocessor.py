import fitz
from PyQt5.QtGui import QPixmap, QImage, QPicture
import os
import sys
from PIL.ImageQt import ImageQt


# Create window


import re
from tqdm import tqdm # pip install tqdm
from PyQt5.Qt import QWidget, QTemporaryDir, QFile, QSqlDatabase, QByteArray,\
    QBuffer, QIODevice, QDataStream
from PyQt5.QtWidgets import QApplication, QLabel, QMessageBox
from PIL.Image import frombytes
from PyQt5.QtSql import QSqlQuery



def populateDeckContent(regex,fulltext,key,suit,principality,arcana,dct):
    if match := re.search(regex, fulltext, re.IGNORECASE):        
        dct[key]=dict(DESCRIPTION=str(match.group(1)),SUIT = suit, PRINCIPALITY=principality, 
                                                                    ARCANA=arcana,IMAGE=None)
        print(str(dct[key]))
        

def processArcanas(fulltext, arcana, dct, startid=0):
    i=startid
    
    regex = r"(?sm)(?:^"+str(i)+"\.\s(\w+(?:-\w*)*)(.*$.*)^"+str(i+1)+"\. )|(?:^"+str(i)+"\.\s(\w+(?:-\w*)*)(.*$.*)\Z)"
    while match := re.search(regex, fulltext, re.IGNORECASE):        
        
        name=match.group(3) if match.group(1)is None else match.group(1)
        body=match.group(4) if match.group(2)is None else match.group(2)
        key=str(name+str(i).zfill(3)).upper()
        dct[key]=body
        print(dct[key])
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
    
    
    
def loadMajorArcanaInfo(buf, dct):
    arcana='MAJOR_ARCANA'
    
    regex = '(?sm)^The\s{1,5}Death\s{1,5}Angels\s{1,5}(.*)^Guide\s{1,5}to\s{1,5}Using'
    suit='DEATH ANGEL'
    
    if match := re.search(regex, buf, re.IGNORECASE):        
        
        subtext=str(match.group(1))
        regex=r'(?i)KHLD\s{1,5}[\W]+(\w+(?:-\w*)*)'
        
        for key in dct.keys():
            if match := re.search(regex.replace('KHLD', key[:-3]), subtext, re.IGNORECASE):
                principality=match.group(1)
                dct[key]=dict(DESCRIPTION=dct[key] ,SUIT = suit, PRINCIPALITY=principality, ARCANA=arcana, IMAGE=None)
        
    
    regex = '(?sm)^The\s{1,5}Archons\s{1,5}(.*)^The\s{1,5}Death'
    suit='ARCHON'
    
    if match := re.search(regex, buf, re.IGNORECASE):        
        
        subtext=str(match.group(1))
        regex=r'(?i)KHLD\s{1,5}[\W]+(\w+(?:-\w*)*)'
        
        for key in dct.keys():
            if match := re.search(regex.replace('KHLD', key[:-3]), subtext, re.IGNORECASE):
                principality=match.group(1)
                dct[key]=dict(DESCRIPTION=dct[key] ,SUIT = suit, PRINCIPALITY=principality, ARCANA=arcana, IMAGE=None)
        
    suit='CREATOR'
    
    principality='METROPOLIS'
    key='ANTHROPOS000'
    dct[key]=dict(DESCRIPTION=dct[key] ,SUIT = suit, PRINCIPALITY=principality, ARCANA=arcana, IMAGE=None)
    
    principality='ELYSIUM'
    key='DEMIURGOS001'
    dct[key]=dict(DESCRIPTION=dct[key] ,SUIT = suit, PRINCIPALITY=principality, ARCANA=arcana, IMAGE=None)
    
    principality='INFERNO'
    key='ASTAROTH002'
    dct[key]=dict(DESCRIPTION=dct[key] ,SUIT = suit, PRINCIPALITY=principality, ARCANA=arcana, IMAGE=None)
    

def loadMinorArcana(buf, dct):
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
                            SUIT = currsuit, PRINCIPALITY=currprincipality, ARCANA=arcana, IMAGE=None)
        


def getpdftext(outputdir, workdir, filename):
    doc = fitz.Document(workdir + filename )
    pages = [ doc[ i ] for i in range( doc.page_count ) ]
    fulltext_buffer=''
    
    
    for page in pages:
        
        t=page.get_textpage()
        
        
        for block in t.extractBLOCKS():
            fulltext_buffer+=str(block[4])
        
    with open(outputdir + filename+'.txt', 'w', encoding="utf-8") as f:
        f.write(fulltext_buffer)

    return fulltext_buffer

def createConnection():

    #QDir::mkpath("../student");    
    #QFile::copy(":/data/kcdata", "")

    tmpDir=QTemporaryDir()
    print("temporary dir:", tmpDir.path())
    
    fcFileCopy=QFile()
    dstFile=QFile('kcdatatest')
    
    if dstFile.exists():
        dstFile.remove()
        
    fcFileCopy.copy("../resources/data/kcdatatest", 'kcdatatest')
    print("copied file:", tmpDir.path() + '/kcdata')
    
    con = QSqlDatabase.addDatabase("QSQLITE")
    #con.setConnectOptions("QSQLITE_OPEN_READONLY")

    con.setDatabaseName( 'kcdatatest')

    if not con.open():

        QMessageBox.critical(

            None,

            "KultOracle - Error!",

            "Database Error: %s" % con.lastError().databaseText(),

        )

        return False

    return True




if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    w = QWidget()
    w.setWindowTitle("PyQT4 Pixmap @ pythonspot.com ")
    
    workdir = "/home/columbus/dev/graphicsdesign/"
    outputdir = "/home/columbus/dev/graphicsdesign/output/"
    deck_rules_filename='KULT Divinity Lost - Tarot Deck Rules.pdf'
    tarot_deck_filename='kult-tarot.pdf'

    fulltext_buffer = ''
    fulltext_major_arcana_buffer = ''
    fulltext_minor_arcana_buffer = ''
    
    deckcontentdct={}

    filename=deck_rules_filename    
    fulltext_buffer = getpdftext(outputdir, workdir, filename )
        
    filename=tarot_deck_filename    
    fulltext_tarot_deck = getpdftext(outputdir, workdir, filename )

    #FRONT COVER
    regex = r"(?s)(Basic\s{1,5}Guidelines.*)Example\s{1,5}reading"
    populateDeckContent(regex,fulltext_buffer,'FRONT COVER003','COVER','ALL','ALL',deckcontentdct)

    #'ARCHONS'
    regex = r"(?sm)Reading\s{1,5}Templates\s{1,5}The\s{1,5}Major\s{1,5}Arcana(.*)^0. "
    populateDeckContent(regex,fulltext_buffer,'ARCHONS002','COVER','ALL','ALL',deckcontentdct)
        
    #'DEATH ANGELS'
    regex = r"(?sm)Reading\s{1,5}Templates\s{1,5}The\s{1,5}Major\s{1,5}Arcana(.*)^0. "
    populateDeckContent(regex,fulltext_buffer,'DEATH ANGELS004','COVER','ALL','ALL',deckcontentdct)
        
    #'SUITS'
    regex = r"(?sm)^The\s{1,5}Minor\s{1,5}Arcana\s{1,5}(The\s{1,5}Minor\s{1,5}Arcana.*)^Skulls"
    populateDeckContent(regex, fulltext_buffer, 'SUITS001','COVER','ALL','ALL', deckcontentdct)
    
    #'KULT GUIDE URL'
    deckcontentdct['KULT GUIDE URL005']='Guide to Using\nthe Tarot Deck\nhttps://kultdivinitylost.com/tarot'
    deckcontentdct['KULT GUIDE URL005']=dict( DESCRIPTION=deckcontentdct['KULT GUIDE URL005'], SUIT='COVER',
                        PRINCIPALITY='ALL',ARCANA='ALL',IMAGE=None)
    
    #'The Major Arcana'
    regex=r"(?sm)(^0\.\s{1,5}\w+(?:-\w*)*$.*)\d{1,3}\s{1,5}^The\s{1,5}Major\s{1,5}Arcana\s{1,5}"
    if match := re.search(regex, fulltext_buffer, re.IGNORECASE):
        fulltext_major_arcana_buffer=match.group(1)    
        processArcanas(fulltext_major_arcana_buffer, 'MAJOR_ARCANA', deckcontentdct)    
        loadMajorArcanaInfo(fulltext_tarot_deck, deckcontentdct)
    
    #'The Minor Arcana'
    regex=r"(?sm)(^1\.\s{1,5}\w+(?:-\w*)*$.*\.)(?:\s{1,5}^\d{1,3}\s{1,5}^The\s{1,5}Minor\s{1,5}Arcana\s{1,5})"
    if match := re.search(regex, fulltext_buffer.replace(fulltext_major_arcana_buffer, ""), re.IGNORECASE):
        fulltext_minor_arcana_buffer=match.group(1)    
        #processArcanas(fulltext_minor_arcana_buffer, 'MINOR_ARCANA',deckcontentdct, 1)
        loadMinorArcana(fulltext_minor_arcana_buffer, deckcontentdct)

    doc = fitz.Document(workdir+tarot_deck_filename)
    toc = doc.get_toc(False)

    
    for toc_page in toc:
        for key in deckcontentdct.keys():
            if key[:-3] in toc_page[1].upper():
                for img in tqdm(doc.get_page_images(toc_page[2]-1), desc="page_images"):
                    xref = img[0]
                    image = doc.extract_image(xref)
                    print(f"\nwidth = {image['width']} height = {image['height']}")
                    
                    if image["width"]==390 and image["height"] == 686:
                        pix = fitz.Pixmap(doc, xref)
                        pix.save(os.path.join(outputdir, "%s_p%s-%s.png" % (deck_rules_filename[:-4], toc_page[2]-1, xref)))
                        pilimg = frombytes('RGB', [pix.width, pix.height], pix.samples,'raw')
                        qimage = ImageQt( pilimg).copy()

                        label = QLabel(w)
                        pixmap = QPixmap.fromImage(qimage)
                        w.resize(pixmap.width(),pixmap.height())
                                                
                        byteArray = QByteArray()
                        buffer =  QBuffer(byteArray)
                        buffer.open(QIODevice.WriteOnly);
                        
                        out = QDataStream (buffer)
                        out << pixmap

                        deckcontentdct[key]['IMAGE'] = byteArray.data()

                        byteArray = QByteArray(deckcontentdct[key]['IMAGE'])
                        buffer =  QBuffer(byteArray)
                        buffer.open(QIODevice.ReadOnly);
                        inp = QDataStream (buffer)                        
                        picdata = QPixmap()
                        inp >> picdata                        
                        
                        label.setPixmap(picdata)
                        # Draw window
                        #w.show()
                        # Create widget
                        #app.exec_()

    if not createConnection():
        sys.exit(1)

    query = QSqlQuery()
    
    prepstmnt= "INSERT INTO CARDS_DECK ( NAME, DESCRIPTION, SUIT, PRINCIPALITY, ARCANA, IMAGE) " + \
                    "VALUES ( ?,?,?,?,?,? )"

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

            print("query insert res: ",query.exec())
        print("query result: ",query.lastError().text())
        


    

    # Draw window
    #w.show()
    # Create widget
    #app.exec_()



    QSqlDatabase.removeDatabase(QSqlDatabase.database().connectionName())

    
    print(deckcontentdct)



