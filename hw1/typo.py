import random

outFile = open('./typo.fst', 'w')

startState = 'START'
endState = 'END'
interState = 'INT'
stateCounter = 0

mistakeDict = {}
typoSeenDict = {}

mistakeDict['A'] = ['Q','S','Z']
mistakeDict['B'] = ['G','H','V','N']
mistakeDict['C'] = ['X','D','F','V']
mistakeDict['D'] = ['E','S','X','C','F','R']
mistakeDict['E'] = ['W','S','D','F','R']
mistakeDict['F'] = ['R','D','C','V','G','T']
mistakeDict['G'] = ['T','F','V','B','H','Y']
mistakeDict['H'] = ['Y','G','B','N','J','U']
mistakeDict['I'] = ['U','J','K','O']
mistakeDict['J'] = ['U','H','N','M','K','I']
mistakeDict['K'] = ['I','J','M','L','O']
mistakeDict['L'] = ['K','O','P']
mistakeDict['M'] = ['N','J','K']
mistakeDict['N'] = ['B','H','J','M']
mistakeDict['O'] = ['I','K','L','P']
mistakeDict['P'] = ['O','L']
mistakeDict['Q'] = ['W','A']
mistakeDict['R'] = ['E','D','F','T']
mistakeDict['S'] = ['W','A','Z','X','D','E']
mistakeDict['T'] = ['R','F','G','Y']
mistakeDict['U'] = ['Y','H','J','K','I']
mistakeDict['V'] = ['C','F','G','B']
mistakeDict['W'] = ['Q','A','S','E']
mistakeDict['X'] = ['Z','D','S','C']
mistakeDict['Y'] = ['T','G','H','U']
mistakeDict['Z'] = ['X','A','S']

outLine = endState+'\n'
outFile.write(outLine)

for key1,val1 in mistakeDict.items():
    stateCounter += 1
    outLine = '('+startState+' ('+str(stateCounter)+' "'+key1+'" "'+key1+'"))\n'
    outFile.write(outLine)
    outLine = '('+str(stateCounter)+' ('+endState+' *e* *e*))\n'
    outFile.write(outLine)
    prevState1 = stateCounter

    for key2,val2 in mistakeDict.items():
            stateCounter += 1
            outLine = '('+str(prevState1)+' ('+str(stateCounter)+' "'+key2+'" "'+key2+'"))\n'
            outFile.write(outLine)
            outLine = '('+str(stateCounter)+' ('+endState+' *e* *e*))\n'
            outFile.write(outLine)
            prevState2 = stateCounter
            
            for key3,val3 in mistakeDict.items():
                if key3 in typoSeenDict:
                    targetState = typoSeenDict[key3]
                    outLine = '('+str(prevState2)+' ('+str(targetState)+' "'+key3+'" *e*))\n'
                    outFile.write(outLine)
                else:
                    stateCounter += 1
                    typoSeenDict[key3] = stateCounter
                    outLine = '('+str(prevState2)+' ('+str(stateCounter)+' "'+key3+'" *e*))\n'
                    outFile.write(outLine)
                    typoList = mistakeDict[key3]
                    probability = 1.0/len(typoList)
                    for typo in typoList:
                        outLine = '('+str(stateCounter)+' ('+interState+' *e* "'+typo+'" '+str(probability)+'))\n'
                        outFile.write(outLine)
                        
            outLine = '('+str(prevState2)+' ('+str(prevState2)+' "_" "_"))\n'
            outFile.write(outLine)
            
    outLine = '('+str(prevState1)+' ('+str(prevState1)+' "_" "_"))\n'
    outFile.write(outLine)

outLine = '('+interState+' ('+startState+' *e* *e*))\n'
outFile.write(outLine)
outLine = '('+interState+' ('+endState+' *e* *e*))\n'
outFile.write(outLine)

outFile.close()
