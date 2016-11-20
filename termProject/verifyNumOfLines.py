shakespeareFile = open('./shakespeare.raw', 'r')
translationFile = open('./translation.raw', 'r')

shakespeareLines = shakespeareFile.readlines()
translationLines = translationFile.readlines()

shakespeareFile.close()
translationFile.close()

playName = ''
pageNum = 'Start'

shakespeareList = []
translationList = []

countLine = 0
pos = 0

# compiling list for shakespeare file
for idx in range(0, len(shakespeareLines)):
    
    line = shakespeareLines[idx]
    line = line.strip()
    
    if line.find('--%%-- Play:')>=0:
        playName = line.replace('--%%--', '')
        playName = playName.replace('Play:', '')
        playName = playName.strip()

    elif line.find('--%%-- pageNum')>=0:
        shakespeareList.extend([(playName, pageNum, countLine)])
        pos += 1
        countLine = 0
        pageNum = line.replace('--%%--', '')
        pageNum = pageNum.replace('pageNum:', '')
        pageNum = pageNum.strip()

    elif len(line)>0:
        countLine += 1

pos = 0
countLine = 0
playName = ''
pageNum = 'Start'

# compiling list for translation file
for idx in range(0, len(translationLines)):
    
    line = translationLines[idx]
    line = line.strip()
    
    if line.find('--%%-- Play:')>=0:
        playName = line.replace('--%%--', '')
        playName = playName.replace('Play:', '')
        playName = playName.strip()

    elif line.find('--%%-- pageNum')>=0:
        translationList.extend([(playName, pageNum, countLine)])
        pos += 1
        countLine = 0
        pageNum = line.replace('--%%--', '')
        pageNum = pageNum.replace('pageNum:', '')
        pageNum = pageNum.strip()

    elif len(line)>0:
        countLine += 1

totalMismatch = 0
print translationList[0]
print shakespeareList[0]
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
