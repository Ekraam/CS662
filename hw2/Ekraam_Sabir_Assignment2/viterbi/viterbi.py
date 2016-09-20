from __future__ import division
import sys

if len(sys.argv)<2:
    print("Give a sentence to decode")
else:
    lenSentence = len(sys.argv) - 1
    print(str(lenSentence)+' tokens receive from user for processing')

sentence = []
for i in range(1, len(sys.argv)):
    sentence.extend([sys.argv[i]])

print(sentence)

inpFile = open('./train-data', 'r')

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

#noisy channel probability
ttwFreqDict = {}
ttwProbDict = {}

#created a nested dictionary with the frequency of each word for a particular tag
for i in lines:
    sep = i.split('/')
    word = sep[0]
    tag = sep[1]
    tag = tag.strip()
    
    if tag in ttwFreqDict:
        
        if word in ttwFreqDict[tag]:
            ttwFreqDict[tag][word] += 1
        else:
            ttwFreqDict[tag][word] = 1

    else:
        
        ttwFreqDict[tag] = {}
        ttwFreqDict[tag][word] = 1

#convert the frequency to probability
for key,val in ttwFreqDict.items():
    totalCount = 0

    for key2,val2 in ttwFreqDict[key].items():
        totalCount += val2

    ttwProbDict[key] = {}

    for key2,val2 in ttwFreqDict[key].items():
        prob = val2/totalCount
        ttwProbDict[key][key2] = prob

m = len(uniqueTags)
n = lenSentence
Q = [[0 for x in range(n)] for y in range(m)] 
best_pred = [[0 for x in range(n)] for y in range(m)] 

uniqueTagList = []
for key,val in uniqueTags.items():
    uniqueTagList.extend([key])

for j in range(0,m):
    tj = uniqueTagList[j]
    if tj in uniProbDict:
        p_tj = uniProbDict[tj]
    else:
        p_tj = 0

    w1 = sentence[0]
    if w1 in ttwProbDict[tj]:
        p_w1tj = ttwProbDict[tj][w1]
    else:
        p_w1tj = 0

    Q[j][0] = p_tj * p_w1tj

for i in range(1,n):
    for j in range(0,m):
        Q[j][i] = 0
        best_pred[j][i] = 0
        best_score = -1
        for k in range(0,m):
            tj = uniqueTagList[j]
            tk = uniqueTagList[k]
            if tk in biProbDict:
                if tj in biProbDict[tk]:
                    p_tjtk = biProbDict[tk][tj]
                else:
                    p_tjtk = 0
            else:
                p_tjtk = 0

            wi = sentence[i]
            if wi in ttwProbDict[tj]:
                p_witj = ttwProbDict[tj][wi]
            else:
                p_witj = 0
            r = p_tjtk * p_witj * Q[k][i-1]

            if r > best_score:
                best_score = r
                best_pred[j][i] = k
                Q[j][i] = r


final_best = 0
final_score = -5
for j in range(0,m):
    if Q[j][n-1] > final_score:
        final_score = Q[j][n-1]
        final_best = j

finalSeq = [uniqueTagList[final_best]]
current = final_best
for i in range(n-1,0,-1):
    current = best_pred[current][i]
    finalSeq.extend([uniqueTagList[current]])

finalSeq.reverse()
print(finalSeq)
print('Score/probability: '+str(final_score))

#get % of cells non-zero
nonZeroCount = 0
for i in range(0,n):
    for j in range(0,m):
        if Q[j][i]!=0:
            nonZeroCount += 1
print('Total cell count for this sentence: '+str(m*n))
print('Total non zero cells: '+str(nonZeroCount))

inpFile.close()

