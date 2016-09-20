from __future__ import division

inpFile = open('./train-data', 'r')
outFile = open('tag-to-word.wfst', 'w')

lines = inpFile.readlines()

freqDict = {}
probDict = {}

#created a nested dictionary with the frequency of each word for a particular tag
for i in lines:
    sep = i.split('/')
    word = sep[0]
    tag = sep[1]
    tag = tag.strip()
    
    if tag in freqDict:
        
        if word in freqDict[tag]:
            freqDict[tag][word] += 1
        else:
            freqDict[tag][word] = 1

    else:
        
        freqDict[tag] = {}
        freqDict[tag][word] = 1

#convert the frequency to probability
for key,val in freqDict.items():
    totalCount = 0

    for key2,val2 in freqDict[key].items():
        totalCount += val2

    probDict[key] = {}

    for key2,val2 in freqDict[key].items():
        prob = val2/totalCount
        probDict[key][key2] = prob

#start building the WFST

stateCounter = 0

outFile.write('STARTEND\n')

for key,val in probDict.items():
    for key2,val2 in probDict[key].items():
        
        outFile.write('(STARTEND (STARTEND "'+key+'" "'+key2+'" '+str(val2)+'))\n')

inpFile.close()
outFile.close()
