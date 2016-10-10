# This code works for the transliteration problem

from __future__ import division
import itertools
import operator


inpFile = open('./epron-jpron-unsupervised.data', 'r')
inpLines = inpFile.readlines()

alignFile = open('./epron-jpron.alignment', 'w')

ejPair = {}
eAlignPair = {}

# alignment section
for i in range(0, len(inpLines), 3):
    
    eline = inpLines[i].strip()
    jline = inpLines[i+1].strip()

    key = eline
    ejPair[eline] = jline

    eline = eline.split()
    jline = jline.split()

    maxNum = len(eline)
    jNum = len(jline)

    extraAlign = jNum - maxNum
    listofNum = []

    for num in range(1, maxNum+1):
        for iter in range(extraAlign):
            listofNum.extend([num])
            
    listAlign = list(itertools.combinations(listofNum, extraAlign))
    uniqAlign = set(listAlign)
    listAlign = list(uniqAlign)

    legalAlignments = {}
    counter = 1

    for perm in listAlign:

        validAlign = []
        for num in range(1, maxNum+1):
            validAlign.extend([num])

        validAlign.extend(perm)

        validAlign = sorted(validAlign, key=int)

        legalAlignments[counter] = validAlign
        counter += 1
        
        if i<10:
            print(eline)
            print(jline)
            print(validAlign)

    eAlignPair[key] = legalAlignments

# EM section

ejPhonProb = {}
ejPhonCount = {}

for iter in range(5):    
    printCount = 0

    for eword,jword in ejPair.items():

        allAlign = eAlignPair[eword] # key: alignment say 1: [1,1,2,2,3]
        allAlignProb = {}

        if iter==0:
            n = len(allAlign)
            for key,align in allAlign.items():
                allAlignProb[key] = 1/n

        else:
            # 1 to n
            for key,align in allAlign.items():
                allAlignProb[key] = 1 # Pai = allAlignProb[key]
                ephon = eword.split()
                jphon = jword.split()
                alignNum = 1

                # 1 to r
                for e in ephon:
                    J = ''
                    idx = [i for i, j in enumerate(align) if j == alignNum]
                    for pos in idx:
                        J += jphon[pos]
                    alignNum += 1
                    allAlignProb[key] *= ejPhonProb[e][J]

            # normalize
            total = 0
            for key,align in allAlign.items():
                total += allAlignProb[key]
            for key,align in allAlign.items():
                allAlignProb[key] = allAlignProb[key]/total

            # print best alignment after every iteration
            if eword in ['"EY" "B" "AH" "L"', '"AH" "B" "AW" "T"', '"AH" "K" "EY" "SH" "AH"', '"EY" "S"', '"AE" "S" "AH" "T" "OW" "N"']:
                key = max(allAlignProb.iteritems(), key=operator.itemgetter(1))[0]
                bestAlignment = allAlign[key]
                print(eword)
                print(jword)
                print(bestAlignment)

            # save the results after 5th iteration
            if iter==4:
                key = max(allAlignProb.iteritems(), key=operator.itemgetter(1))[0]
                bestAlignment = allAlign[key]
                alignFile.write(eword+'\n')
                alignFile.write(jword+'\n')
                for num in bestAlignment:
                    alignFile.write(str(num)+' ')
                alignFile.write('\n')


        # fractional counts
        for key,align in allAlign.items():
            ephon = eword.split()
            jphon = jword.split()
            alignNum = 1
                        
            for e in ephon:
                J = ''
                idx = [i for i, j in enumerate(align) if j == alignNum]
                for pos in idx:
                    J += jphon[pos]
                alignNum += 1

                if e in ejPhonCount:
                    if J in ejPhonCount[e]:
                        ejPhonCount[e][J] += allAlignProb[key]
                    else:
                        ejPhonCount[e][J] = allAlignProb[key]
                else:
                    ejPhonCount[e] = {}
                    ejPhonProb[e] = {}
                    ejPhonCount[e][J] = allAlignProb[key]
                    ejPhonProb[e][J] = 0

    # normalize sound translation
    for e,allJSeq in ejPhonCount.items():
        total = 0
        for J, count in allJSeq.items():
            total += count
        for J, count in allJSeq.items():
            ejPhonProb[e][J] = count/total;

    for e,allJSeq in ejPhonCount.items():
        for J, count in allJSeq.items():
            ejPhonCount[e][J] = 0

alignFile.close()

# get accuracy compared to epron-jpron.data
refFile = open('./epron-jpron.data', 'r')
alignFile = open('./epron-jpron.alignment', 'r')

refLines = refFile.readlines()
hypLines = alignFile.readlines()

wordCount = 0
tokenCount = 0
corrWordCount = 0
corrTokenCount = 0

for i in range(0, len(refLines), 3):
    refLine = refLines[i]
    refLine = refLine.strip()
    
    for j in range(0, len(hypLines), 3):
        hypLine = hypLines[j]
        hypLine = hypLine.strip()

        if refLine==hypLine:
            refAlign = refLines[i+2]
            refAlign = refAlign.strip()
            hypAlign = hypLines[j+2]   
            hypAlign = hypAlign.strip()
            if len(refAlign)==len(hypAlign):
                wordCount += 1
                if (refAlign==hypAlign):
                    corrWordCount += 1
                for k in range(len(refAlign)):
                    refchar = refAlign[k]
                    hypchar = hypAlign[k]
                    if refchar!=' ':
                        tokenCount += 1
                        if refchar==hypchar:
                            corrTokenCount += 1

print("Word accuracy "+str(100*corrWordCount/wordCount)+"%")
print("Token level accuracy "+str(100*corrTokenCount/tokenCount)+"%")

inpFile.close()
alignFile.close()

# section on making epron-jpron-unsupervised.wfst

wfstFile = open('./epron-jpron-unsupervised.wfst', 'w')

wfstFile.write('SE\n')
stateCounter = 0
prevStateCounter = 0

for e, allJSeq in ejPhonProb.items():    
    for J,prob in allJSeq.items():

        if prob>0.01:
            idx = [i for i, ltr in enumerate(J) if ltr == '"']

            if len(idx)%2!=0:
                print('Odd number of " found')

            for i in range(0,len(idx),2):
                token = J[idx[i]:idx[i+1]+1]
                if len(idx)==2:
                    wfstFile.write('(SE (SE '+e+' '+token+' '+str(prob)+'))\n')
                elif i==0:
                    wfstFile.write('(SE ('+str(stateCounter)+' '+e+' '+token+' '+str(prob)+'))\n')
                    prevStateCounter = stateCounter
                    stateCounter += 1;
                elif i<(len(idx)-2):
                    wfstFile.write('('+str(prevStateCounter)+' ('+str(stateCounter)+' *e* '+token+'))\n')
                    prevStateCounter = stateCounter
                    stateCounter += 1
                elif i==(len(idx)-2):
                    wfstFile.write('('+str(prevStateCounter)+' (SE *e* '+token+'))\n')
                else:
                    print('Unaccounted case found')

wfstFile.close()
