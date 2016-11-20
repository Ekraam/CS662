# This script builds a translation model with 
# model 1 from SMT workbook/662 notebook

from __future__ import division

inpFile1 = open('./shakespeare.data', 'r')
inpFile2 = open('./translation.data', 'r')

shakespeareLines = inpFile1.readlines()
translationLines = inpFile2.readlines()

inpFile1.close()
inpFile2.close()

transProb = {}

# collect frequency
for idx in range(0, len(shakespeareLines)):
    
    shLine = shakespeareLines[idx]
    tnLine = translationLines[idx]

    shLine = shLine.split()
    tnLine = tnLine.split()

    for shWord in shLine:
        for tnWord in tnLine:
            
            if shWord in transProb:
                if tnWord in transProb[shWord]:
                    transProb[shWord][tnWord] += 1
                else:
                    transProb[shWord][tnWord] = 1
            else:
                transProb[shWord] = {}
                transProb[shWord][tnWord] = 1

# collect probability
total = 0
for shWord, innerDict in transProb.items():
    total = 0
    for tnWord, freq in innerDict.items():
        total += freq
    for tnWord, freq in innerDict.items():
        transProb[shWord][tnWord] = freq/total

print transProb
