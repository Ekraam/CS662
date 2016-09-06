inpFile = open('/home/student/cs662/hw1/spanishvocab.txt', 'r')
outFile = open('/home/student/cs662/hw1/finalFSA.fsa', 'w')

stringDic = {}
stateCounter = 0
endState = 'END'

outFile.write(endState+'\n')

def extendFSA(stringSoFar, fullString):
    
    global stringDic
    global stateCounter
    global endState

    startPos = len(stringSoFar)
    remainingString = fullString[startPos:]

    if len(remainingString) != 0:

        if stringSoFar in stringDic:
            startState = stringDic[stringSoFar]
        else:
            startState = 0
            
        lenRemString = len(remainingString)
            
        for pos in range(lenRemString-1):
            char = remainingString[pos:pos+1]
            stateCounter += 1
            stringSoFar += char
            line = '('+str(startState)+' ('+str(stateCounter)+' "'+char+'"))\n'
            outFile.write(line)
            startState = stateCounter
            stringDic[stringSoFar] = stateCounter

        char = remainingString[lenRemString-1:]
        stringSoFar += char
        line = '('+str(startState)+' ('+str(endState)+' "'+char+'"))\n'
        outFile.write(line)
        stringDic[stringSoFar] = endState

    else:
        
        startState = stringDic[stringSoFar]
        line = '('+str(startState)+' ('+str(endState)+' *e*))\n'
        outFile.write(line)

words = []
wordDict = {}

for line in inpFile:
    line = line.strip()
    line = line.replace(' ', '')
    if line in wordDict:
        print('Repeat Word')
    else:
        words.extend([line])
        wordDict[line] = 1

words.sort(key=len)

for fullString in reversed(words):
    print(fullString)
    stringSoFar = fullString
    extending = False

    while stringSoFar != '':
        if stringSoFar in stringDic:
            extending = True
            extendFSA(stringSoFar, fullString)
            break
        else:
            stringSoFar = stringSoFar[:len(stringSoFar)-1]

    if extending==False:
        extendFSA(stringSoFar, fullString)

inpFile.close()
outFile.close()
