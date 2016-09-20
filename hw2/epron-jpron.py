from __future__ import division

inpFile = open('./epron-jpron.data', 'r')
outFile = open('./epron-jpron.wfst', 'w')

lines = inpFile.readlines()
numLines = len(lines)

print("File has "+str(numLines)+' lines')

freqDict = {}
probDict = {}

for i in xrange(0,numLines,3):
    epronList = lines[i].split()
    jpronList = lines[i+1].split()
    alignment = lines[i+2].split()
    for epron in epronList:
        pos = epronList.index(epron)
        pos += 1
        pos = str(pos)
        
        indexes = [i for i,x in enumerate(alignment) if x==pos]
        jpron = ''
        for idx in indexes:
            jpron = jpron+' '+jpronList[idx]

        if epron in freqDict:
            
            if jpron in freqDict[epron]:
                freqDict[epron][jpron] += 1
            else:
                freqDict[epron][jpron] = 1

        else:
            
            freqDict[epron] = {}
            freqDict[epron][jpron] = 1

for key,val in freqDict.items():
    
    totalCount = 0
    
    for key2,val2 in freqDict[key].items():
        totalCount += val2

    probDict[key] = {}

    for key2,val2 in freqDict[key].items():
        prob = val2/totalCount
        if prob>0.01:
            probDict[key][key2] = prob

#start builfing the wfst

stateCounter = 0

outFile.write('STARTEND\n')

for key,val in probDict.items():
    for key2,val2 in probDict[key].items():
        
        pronList = key2.split()
        
        if len(pronList)==1:
            outFile.write('(STARTEND (STARTEND '+key+' '+pronList[0]+' '+str(val2)+'))\n')
        
        elif len(pronList)==2:
            outFile.write('(STARTEND ('+str(stateCounter)+' '+key+' '+pronList[0]+' '+str(val2)+'))\n')
            outFile.write('('+str(stateCounter)+' (STARTEND *e* '+pronList[1]+'))\n')
            stateCounter += 1

        elif len(pronList)>2:

            outFile.write('(STARTEND ('+str(stateCounter)+' '+key+' '+pronList[0]+' '+str(val2)+'))\n')
            
            numOfStates = len(pronList)
            for i in range(1,numOfStates-1):
                outFile.write('('+str(stateCounter)+' ('+str(stateCounter+1)+' *e* '+pronList[i]+'))\n')
                stateCounter += 1

            outFile.write('('+str(stateCounter)+' (STARTEND *e* '+pronList[numOfStates-1]+'))\n')

            stateCounter += 1

        else:
            print('Unexpected Case encountered!')
        

inpFile.close()
outFile.close()
