# this script will process raw files and segment them

import re
import subprocess

shakespeareFile = open('./shakespeare.raw', 'r')
translationFile = open('./translation.raw', 'r')
outputShakespeare = open('./shakespeare.data', 'w')
outputTranslation = open('./translation.data', 'w')

shakespeareLines = shakespeareFile.readlines()
translationLines = translationFile.readlines()

shakespeareFile.close()
translationFile.close()

tempPlayName = ''
playName = ''
pageNum = 'Start'

shakespeareList = []
translationList = []

countLine = 0

# compiling list for shakespeare file
for idx in range(0, len(shakespeareLines)):
    
    line = shakespeareLines[idx]
    line = line.strip()
    
    if line.find('--%%-- Play:')>=0:
        tempPlayName = line.replace('--%%--', '')
        tempPlayName = tempPlayName.replace('Play:', '')
        tempPlayName = tempPlayName.strip()

    elif line.find('--%%-- pageNum')>=0:
        shakespeareList.extend([(playName, pageNum, countLine)])
        countLine = 0
        pageNum = line.replace('--%%--', '')
        pageNum = pageNum.replace('pageNum:', '')
        pageNum = pageNum.strip()
        playName = tempPlayName

    elif len(line)>0:
        countLine += 1

countLine = 0
tempPlayName = ''
playName = ''
pageNum = 'Start'

# compiling list for translation file
for idx in range(0, len(translationLines)):
    
    line = translationLines[idx]
    line = line.strip()
    
    if line.find('--%%-- Play:')>=0:
        tempPlayName = line.replace('--%%--', '')
        tempPlayName = tempPlayName.replace('Play:', '')
        tempPlayName = tempPlayName.strip()

    elif line.find('--%%-- pageNum')>=0:
        translationList.extend([(playName, pageNum, countLine)])
        countLine = 0
        pageNum = line.replace('--%%--', '')
        pageNum = pageNum.replace('pageNum:', '')
        pageNum = pageNum.strip()
        playName = tempPlayName

    elif len(line)>0:
        countLine += 1

totalMismatch = 0

'''
# compare the number of lines in both the lists
if len(translationList)!=len(shakespeareList):
    print 'unequal number of pages found in both lists'
else:
    for idx in range(0, len(translationList)):
        shakespeareCount = shakespeareList[idx][2]
        translationCount = translationList[idx][2]

        if shakespeareCount!=translationCount:
            print 'Mismatched number of lines found in:'
            print shakespeareList[idx][0]
            print shakespeareList[idx][1]
            print 'Shakespeare Count: '+str(shakespeareCount)+' Translation Count: '+str(translationCount)
            totalMismatch += 1

    print 'Total Mismatch: '+str(totalMismatch)
'''

# starting extraction, processing and segmentation

# list to store the processed lines
shakespeareProc = []
translationProc = []

# list of all the pages to exlude from processing
pagesToExclude = []
for idx in range(0, len(translationList)):
    shakespeareCount = shakespeareList[idx][2]
    translationCount = translationList[idx][2]
    if shakespeareCount!=translationCount:
        pageInfo = shakespeareList[idx]
        pagesToExclude.extend([(pageInfo[0], pageInfo[1])])

# temporary name and page variable
playName = ''
pageNum = ''

# extract relevant lines

# shakespeare
for line in shakespeareLines:
    
    line = line.strip()

    if line.find('--%%-- Play:')>=0:
        playName = line.replace('--%%--', '')
        playName = playName.replace('Play:', '')
        playName = playName.strip()

    elif line.find('--%%-- pageNum')>=0:
        pageNum = line.replace('--%%--', '')
        pageNum = pageNum.replace('pageNum:', '')
        pageNum = pageNum.strip()

    elif len(line)>0:

        currentPageInfo = (playName, pageNum)
        
        if currentPageInfo in pagesToExclude:
            continue
        else:
            shakespeareProc.extend([line])

playName = ''
pageNum = ''

# translation
for line in translationLines:
    
    line = line.strip()

    if line.find('--%%-- Play:')>=0:
        playName = line.replace('--%%--', '')
        playName = playName.replace('Play:', '')
        playName = playName.strip()

    elif line.find('--%%-- pageNum')>=0:
        pageNum = line.replace('--%%--', '')
        pageNum = pageNum.replace('pageNum:', '')
        pageNum = pageNum.strip()

    elif len(line)>0:

        currentPageInfo = (playName, pageNum)
        
        if currentPageInfo in pagesToExclude:
            continue
        else:
            translationProc.extend([line])

# process all the lines for spaces, punctuations etc

for idx in range(0, len(shakespeareProc)):
    
    shLine = shakespeareProc[idx]
    tnLine = translationProc[idx]

    shLine = shLine.lower()
    tnLine = tnLine.lower()
    shLine = shLine.replace('!', ' ! ')
    tnLine = tnLine.replace('!', ' ! ')
    shLine = shLine.replace('"', ' " ')
    tnLine = tnLine.replace('"', ' " ')
    shLine = shLine.replace('%', ' % ')
    tnLine = tnLine.replace('%', ' % ')
    shLine = shLine.replace('&', ' & ')
    tnLine = tnLine.replace('&', ' & ')
    shLine = shLine.replace('(', ' ( ')
    tnLine = tnLine.replace('(', ' ( ')
    shLine = shLine.replace(')', ' ) ')
    tnLine = tnLine.replace(')', ' ) ')
    shLine = shLine.replace('-', ' - ')
    tnLine = tnLine.replace('-', ' - ')
    shLine = shLine.replace(',', ' , ')
    tnLine = tnLine.replace(',', ' , ')
    shLine = shLine.replace('.', ' . ')
    tnLine = tnLine.replace('.', ' . ')
    shLine = shLine.replace(';', ' ; ')
    tnLine = tnLine.replace(';', ' ; ')
    shLine = shLine.replace(':', ' : ')
    tnLine = tnLine.replace(':', ' : ')
    shLine = shLine.replace('?', ' ? ')
    tnLine = tnLine.replace('?', ' ? ')

    tnLine = ' '.join(tnLine.split())
    shLine = ' '.join(shLine.split())

    shakespeareProc[idx] = shLine
    translationProc[idx] = tnLine

# take paragraph and segment into sentences for processing

# function to segment a paragraph into sentences
def lineSegment(para):
    
    tempPara = []
    sentence = ''
    for char in para:
        if char=='!' or char=='.' or char=='?' or char=='"':
            sentence += char
            tempPara.extend([sentence])
            sentence = ''
        else:
            sentence += char

    if sentence!='':
        tempPara.extend([sentence])

    return tempPara

sentenceNum = 0
for idx in range(0, len(shakespeareProc)):
    
    shLine = shakespeareProc[idx]
    tnLine = translationProc[idx]
    
    shPara = lineSegment(shLine)
    tnPara = lineSegment(tnLine)

    shakespearePara = open('./shakespearePara.txt', 'w')
    translationPara = open('./translationPara.txt', 'w')
    
    for line in shPara:
        shakespearePara.write(line+'\n')
    for line in tnPara:
        translationPara.write(line+'\n')

    shakespearePara.close()
    translationPara.close()

    subprocess.check_call('./hunalign-1.1/src/hunalign/hunalign hunalign-1.1/data/null.dic ./shakespearePara.txt ./translationPara.txt -realign -text > ./align.txt', shell=True)

    align = open('./align.txt', 'r')
    alignLines = align.readlines()
    align.close()

    alignedShakespeareLines = []
    alignedTranslationLines = []

    shakespearePara = open('./shakespearePara.txt', 'r')
    translationPara = open('./translationPara.txt', 'r')
    
    for line in alignLines:
        tempLine = line.split('\t')
        shakespeareLine = tempLine[0]
        translationLine = tempLine[1]
        shakespeareLine = shakespeareLine.replace('~~~', '')
        translationLine = translationLine.replace('~~~', '')
        if len(shakespeareLine)>0 and len(translationLine)>0:
            outputShakespeare.write(str(sentenceNum)+'_:'+shakespeareLine+'\n')
            outputTranslation.write(str(sentenceNum)+'_:'+translationLine+'\n')
        sentenceNum += 1
    
    shakespearePara.close()
    translationPara.close()

outputShakespeare.close()
outputTranslation.close()
