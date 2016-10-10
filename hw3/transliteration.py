# This code works for the transliteration problem

import itertools
from __future__ import division

inpFile = open('./epron-jpron-unsupervised.data', 'r')
inpLines = inpFile.readlines()

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

print(eAlignPair)

# EM section

ejPhonProb = {}

for iter in range(5):
    
    for eword,jword in ejPair.items():

        allAlign = eAlignPair[eword]
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
                        J += jphon[pos-1]
                    alignNum += 1
                    allAlignProb[key] *= ejPhonProb[e][J]

            # normalize
            total = 0
            for key,align in allAlign.items():
                total += allAlignProb[key]
            for key,align in allAlign.items():
                allAlignProb[key] = allAlignProb[key]/total

            # print best alignment
            
                    
            

inpFile.close()
