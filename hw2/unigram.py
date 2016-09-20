from __future__ import division

inpFile = open('./train-data', 'r')
outFile = open('./unigram.wfsa', 'w')

lines = inpFile.readlines()

freqDict = {}
probDict = {}
totalCount = 0

#create a dictionary with the frequency of each tag in it
for i in lines:
    sep = i.split('/')
    tag = sep[1]
    tag = tag.strip()
    totalCount += 1

    if tag in freqDict:
        freqDict[tag] += 1
    else:
        freqDict[tag] = 1

#convert the frequency to probability
for key,val in freqDict.items():
    prob = val/totalCount
    probDict[key] = prob

#build the wfsa
stateCounter = 0

outFile.write('STARTEND\n')

for key,val in probDict.items():

    outFile.write('(STARTEND (STARTEND "'+key+'" '+str(val)+'))\n')

inpFile.close()
outFile.close()
