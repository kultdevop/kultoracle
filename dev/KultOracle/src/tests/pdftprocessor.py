import fitz

import re



def populateDeckContent(regex,fulltext,key,suit,principality,arcana,dct):
    if match := re.search(regex, fulltext, re.IGNORECASE):        
        dct[key]=(str(match.group(1)),suit,principality,arcana)
        print(str(dct[key]))
        

def processArcanas(fulltext, arcana, dct, startid=0):
    i=startid
    regex = r"(?sm)^("+i+".\s(.+)$.*)^"+(i+1)+". "
    while match := re.search(regex, fulltext, re.IGNORECASE):        
        
        dct[str(match.group(1))]=str(match.group(2))
        print(str(dct[str(match.group(1))]))
        i+=1
        
        regex = r"(?sm)^("+i+".\s(.+)$.*)^"+(i+1)+". "

def loadMajorArcanaInfo(buf, dct):
    arcana='MAJOR_ARCANA'
    
    regex = '(?sm)^The\s{1,5}Death\s{1,5}Angels\s{1,5}(.*)^Guide\s{1,5}to\s{1,5}Using'
    suit='DEATH ANGEL'
    
    if match := re.search(regex, buf, re.IGNORECASE):        
        
        subtext=str(match.group(1))
        regex=r'\s{1,5}[\W]+(\w+)'
        
        for key in dct.keys():
            if match := re.search(key+regex, subtext, re.IGNORECASE):
                principality=match.group(1)
                dct[key]=(str(dct[key]),suit,principality,arcana)
        
    
    regex = '(?sm)^The\s{1,5}Archons\s{1,5}(.*)^The\s{1,5}Death'
    suit='ARCHON'
    
    if match := re.search(regex, buf, re.IGNORECASE):        
        
        subtext=str(match.group(1))
        regex=r'\s{1,5}[\W]+(\w+)'
        
        for key in dct.keys():
            if match := re.search(key+regex, subtext, re.IGNORECASE):
                principality=match.group(1)
                dct[key]=(str(dct[key]),suit,principality,arcana)
        
        
def loadMinorArcana(buf, dct):
    arcana='MINOR_ARCANA'
    suits=('SKULL','ROSE','HOURGLASS','CRESCENT','EYE')
    regex = r'(?sm)(?:^1\. )(.*?)((?=^1\. )|\z)'
    regexextractsuitdesc = r'(?sm)SUITPLH(.*?)(?=^\d+\.)'
    suit='SKULLS'
    
    for match in re.findall(regex, buf, re.IGNORECASE):        
        
        subtext=str(match.group(1))
        currsuit=''
        suitdesc=''
        for suit in suits:
            if match := re.search(regexextractsuitdesc, 
                                  subtext.replace('SUITPLH', suit[0]), re.IGNORECASE):
                suitdesc=match.group(1)
                currsuit=suit[0]
                currprincipality=suit[1]
                break
        
        subtext = subtext.replace(suitdesc,'')
        
        regex_card='(?sm)(^\d+\. \w+)(.*?)((?=^\d+\. )|\Z)'
        
        for match_card in re.findall(regex_card, subtext, re.IGNORECASE):
            dct[match_card.group(1)]=(suitdesc + '\n\n' +match_card.group(2),currsuit,currprincipality)
        
        
        for key in dct.keys():
            if match := re.search(key+regex, subtext, re.IGNORECASE):
                principality=match.group(1)
                dct[key]=(str(dct[key]),suit,principality,arcana)
        

if __name__ == '__main__':
    
    workdir = "/home/columbus/dev/graphicsdesign"
    outputdir = "/home/columbus/dev/graphicsdesign/output"
    deck_rules_filename='/KULT Divinity Lost - Tarot Deck Rules.pdf'
    tarot_deck_filename='/kult-tarot.pdf'
    filename=tarot_deck_filename
    
    doc = fitz.open(workdir + filename )
    pages = [ doc[ i ] for i in range( doc.page_count ) ]
    
        
    fulltext_buffer = ''
    fulltext_major_arcana_buffer = ''
    fulltext_minor_arcana_buffer = ''
    
    deckcontentdct={}
    
    
    for page in pages:
        
        t=page.get_textpage()
        
        
        for block in t.extractBLOCKS():
            fulltext_buffer+=str(block[4])
        
    with open(outputdir + filename+'.txt', 'w', encoding="utf-8") as f:
        f.write(fulltext_buffer)
        
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
    processArcanas(fulltext_major_arcana_buffer, 'MAJOR_ARCANA', deckcontentdct)
    
    loadMajorArcanaInfo(fulltext_major_arcana_buffer, deckcontentdct)
    
    
    #'The Minor Arcana'
    processArcanas(fulltext_minor_arcana_buffer, 'MINOR_ARCANA',deckcontentdct, 1)
    
    loadMinorArcana(fulltext_minor_arcana_buffer, deckcontentdct)
    
    print(deckcontentdct)



    
