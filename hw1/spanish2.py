import time
import sys

inpFile = open('/home/student/cs662/hw1/spanishvocab.txt', 'r')
outFile = open('/home/student/cs662/hw1/spanish2.fsa', 'w')

startStringDict = {}
endStringDict = {}

stateCounter = 0

outFile.write('END\n')

def extendFSA(stringSoFar, backString, fullString):

    if fullString=='RESPETABLES' or fullString=='ABDOMINALES':
        print(stringSoFar)
        print(backString)
        print(fullString)

    global stateCounter
    global startStringDict
    global endStringDict
    
    startPos = len(stringSoFar)
    endPos = len(fullString) - len(backString)
    remainingString = fullString[startPos:endPos]
    endString = remainingString+backString
    if (stringSoFar+remainingString+backString)!=fullString:
        print('String Decomposition Wrong')
        print('Full String '+fullString)
        print('Start String '+stringSoFar)
        print('middle String '+remainingString)
        print('End String '+backString)

    if fullString=='RESPETABLES' or fullString=='ABDOMINALES':
        print(remainingString)
        print(endString)

    if stringSoFar in startStringDict:
        startState = startStringDict[stringSoFar]
    elif stringSoFar == '':
        startState = 0
    else:
        print('Non empty start not found')
        sys.exit()
        
    if backString in endStringDict:
        endState = endStringDict[backString]
    elif backString == '':
        endState = 'END'
    else:
        print('Non empty end not found')
        sys.exit()

    if len(remainingString) != 0:
        
        lenRemString = len(remainingString)

        for pos in range(lenRemString-1):
            char = remainingString[pos]
            
            if len(char) != 1:
                print('Char error')
                sys.exit()

            stateCounter += 1
            stringSoFar += char
            line = '('+str(startState)+' ('+str(stateCounter)+' "'+char+'"))\n'
            outFile.write(line)
            endStringDict[endString] = startState
            startStringDict[stringSoFar] = stateCounter
            startState = stateCounter
            endString = endString[1:]

        char = remainingString[lenRemString-1]
        stringSoFar += char
        line = '('+str(startState)+' ('+str(endState)+' "'+char+'"))\n'
        outFile.write(line)
        endStringDict[endString] = startState
        startStringDict[stringSoFar] = endState

    else:
        
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
    stringSoFar = fullString
    backString = fullString

    while stringSoFar != '':
        if stringSoFar in startStringDict:
            break
        stringSoFar = stringSoFar[:len(stringSoFar)-1]
            
    while backString != '':
        if backString in endStringDict:
            break
        backString = backString[1:]

    if (len(backString)+len(stringSoFar))<=len(fullString):
        extendFSA(stringSoFar, backString, fullString)

    elif len(stringSoFar)>=len(backString):
        backString = fullString[len(stringSoFar):]
        addition = len(backString)+len(stringSoFar)
        if addition!=len(fullString):
            print("Miscalculation")
            print(stringSoFar)
            print(backString)
            print(fullString)
            break
        extendFSA(stringSoFar, backString, fullString)

    elif len(stringSoFar)<len(backString):
        stringSoFar = fullString[:len(fullString)-len(backString)]
        addition = len(backString)+len(stringSoFar)
        if addition!=len(fullString):
            print("Miscalculation")
            print(stringSoFar)
            print(backString)
            break
        extendFSA(stringSoFar, backString, fullString)
    else:
        print('Unkown Case found')
        sys.exit()
        
    if fullString =='RESPETABLES':
        print("stringSoFar "+stringSoFar)
        print("backString "+backString)

    '''if len(stringSoFar)==0 and len(backString)==0:
        extendFSA(stringSoFar, fullStringAfterBackMatch, fullString, 'START', 'END')

    #elif stringSoFar == backString and stringSoFar == fullString:
    #    extendFSA(stringSoFar, fullStringAfterBackMatch, fullString, tempStartState, 'END')

    elif len(stringSoFar)>=len(backString) and backString != '':
        extendFSA(stringSoFar, fullStringAfterBackMatch, fullString, tempStartState, tempEndState)

    elif len(stringSoFar)>=len(backString) and backString == '':
        extendFSA(stringSoFar, fullStringAfterBackMatch, fullString, tempStartState, 'END')

    elif len(stringSoFar)<len(backString) and stringSoFar != '':
        extendFSA(stringSoFar, fullStringAfterBackMatch, fullString, tempStartState, tempEndState)

    elif len(stringSoFar)<len(backString) and stringSoFar == '':
        extendFSA(stringSoFar, fullStringAfterBackMatch, fullString, 'START', tempEndState)

    else:
        print('Unknown Case Encountered')
        sys.exit()'''

line = '(END (START "_"))\n'
outFile.write(line)

inpFile.close()
outFile.close()

if '' in endStringDict:
    print(endStringDict[''])
if '' in startStringDict:
    print(startStringDict[''])
