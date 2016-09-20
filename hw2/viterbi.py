from __future__ import division

inpFile = open('./train-data', 'r')
outFile = open('./bigram.wfsa', 'w')

lines = inpFile.readlines()

uniFreqDict = {}
uniProbDict = {}
biFreqDict = {}
biProbDict = {}
uniqueTags = {}

#create dictionaries with frequency of unigram and bigram tags
line = lines[0].split('/')
tag = line[1]
tag = tag.strip()
uniFreqDict[tag] = 1
uniCount = 1
stateCounter = 0
uniqueTags[tag] = stateCounter
stateCounter += 1

for i in range(1, len(lines)):
    line = lines[i-1].split('/')
    tag1 = line[1]
    tag1 = tag1.strip()

    line = lines[i].split('/')
    tag2 = line[1]
    tag2 = tag2.strip()

    if tag2 not in uniqueTags:
        uniqueTags[tag2] = stateCounter
        stateCounter += 1

    if tag1 is '.':
        uniCount += 1
        if tag2 in uniFreqDict:
            uniFreqDict[tag2] += 1
        else:
            uniFreqDict[tag2] = 1

    else:
        if tag1 in biFreqDict:
            
            if tag2 in biFreqDict[tag1]:
                biFreqDict[tag1][tag2] += 1
            else:
                biFreqDict[tag1][tag2] = 1

        else:
            biFreqDict[tag1] = {}
            biFreqDict[tag1][tag2] = 1

#convert the freq to probability
for key,val in uniFreqDict.items():
    prob = val/uniCount
    uniProbDict[key] = prob

for key,val in biFreqDict.items():
    totalCount = 0
    for key2,val2 in biFreqDict[key].items():
        totalCount += val2

    biProbDict[key] = {}

    for key2,val2 in biFreqDict[key].items():
        prob = val2/totalCount
        biProbDict[key][key2] = prob



inpFile.close()
outFile.close()
