import fitz

import re



def populateDeckContent(regex,fulltext,key,suit,principality,arcana,dct):
    if match := re.search(regex, fulltext, re.IGNORECASE):        
        dct[key]=(str(match.group(1)),suit,principality,arcana)
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
                dct[key]=(dct[key],suit,principality,arcana)
        
    
    regex = '(?sm)^The\s{1,5}Archons\s{1,5}(.*)^The\s{1,5}Death'
    suit='ARCHON'
    
    if match := re.search(regex, buf, re.IGNORECASE):        
        
        subtext=str(match.group(1))
        regex=r'(?i)KHLD\s{1,5}[\W]+(\w+(?:-\w*)*)'
        
        for key in dct.keys():
            if match := re.search(regex.replace('KHLD', key[:-3]), subtext, re.IGNORECASE):
                principality=match.group(1)
                dct[key]=(dct[key],suit,principality,arcana)
        
    suit='CREATOR'
    
    principality='METROPOLIS'
    key='ANTHROPOS000'
    dct[key]=(dct[key],suit,principality,arcana)
    
    principality='ELYSIUM'
    key='DEMIURGE001'
    dct[key]=(dct[key],suit,principality,arcana)
    
    principality='INFERNO'
    key='ASTAROTH002'
    dct[key]=(dct[key],suit,principality,arcana)
    

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
            dct[match_card[2] + match_card[1].zfill(3)]=(suitdesc + '\n\n' +match_card[0],currsuit,currprincipality,arcana)
        


def getpdftext(outputdir, workdir, filename):
    doc = fitz.open(workdir + filename )
    pages = [ doc[ i ] for i in range( doc.page_count ) ]
    fulltext_buffer=''
    
    
    for page in pages:
        
        t=page.get_textpage()
        
        
        for block in t.extractBLOCKS():
            fulltext_buffer+=str(block[4])
        
    with open(outputdir + filename+'.txt', 'w', encoding="utf-8") as f:
        f.write(fulltext_buffer)

    return fulltext_buffer

if __name__ == '__main__':
    
    workdir = "/home/columbus/dev/graphicsdesign"
    outputdir = "/home/columbus/dev/graphicsdesign/output"
    deck_rules_filename='/KULT Divinity Lost - Tarot Deck Rules.pdf'
    tarot_deck_filename='/kult-tarot.pdf'

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
    populateDeckContent(regex,fulltext_buffer,'FRONT COVER','COVER','ALL','ALL',deckcontentdct)

    #'ARCHONS'
    regex = r"(?sm)Reading\s{1,5}Templates\s{1,5}The\s{1,5}Major\s{1,5}Arcana(.*)^0. "
    populateDeckContent(regex,fulltext_buffer,'ARCHONS','COVER','ALL','ALL',deckcontentdct)
        
    #'DEATH ANGELS'
    regex = r"(?sm)Reading\s{1,5}Templates\s{1,5}The\s{1,5}Major\s{1,5}Arcana(.*)^0. "
    populateDeckContent(regex,fulltext_buffer,'DEATH ANGELS','COVER','ALL','ALL',deckcontentdct)
        
    #'SUITS'
    regex = r"(?sm)^The\s{1,5}Minor\s{1,5}Arcana\s{1,5}(The\s{1,5}Minor\s{1,5}Arcana.*)^Skulls"
    populateDeckContent(regex, fulltext_buffer, 'SUITS','COVER','ALL','ALL', deckcontentdct)
    
    #'KULT GUIDE URL'
    deckcontentdct['KULT GUIDE URL']='Guide to Using\nthe Tarot Deck\nhttps://kultdivinitylost.com/tarot'
    deckcontentdct['KULT GUIDE URL']=(deckcontentdct['KULT GUIDE URL'],'COVER','ALL','ALL')
    
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
    
    print(deckcontentdct)
