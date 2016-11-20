# this script collects unigram and bigram probabilities for language model

from __future__ import division

inpFile = open('./shakespeare.data', 'r')
outFile = open('./shakespeare.wfsa', 'w')

shakespeareLines = inpFile.readlines()

inpFile.close()

unigramProb = {}
bigramProb = {}
uniqueState = {}
stateCounter = 0

# collect frequency
for lines in shakespeareLines:

    lines = lines.strip()
    lines = lines.split('_:')
    
    if len(lines)>2:
        print 'extra delimiter line found'
        print lines
        continue
    else:
        lines = lines[1]

    lines = lines.split()
    
    # start word prob
    word = lines[0]
    if word in unigramProb:
        unigramProb[word] += 1
    else:
        unigramProb[word] = 1

    # bigram end word prob
    word = lines[-1]
    # if words don't have state of their own then add it
    if word not in uniqueState:
        uniqueState[word] = stateCounter
        stateCounter += 1

    if word in bigramProb:
        if 'END' in bigramProb:
            bigramProb[word]['END'] += 1
        else:
            bigramProb[word]['END'] = 1
    else:
        bigramProb[word] = {}
        bigramProb[word]['END'] = 1

    # bigram prob
    for idx in range(0, len(lines)-1):
        
        word1 = lines[idx]
        word2 = lines[idx+1]

        # if words don't have state of their own then add it
        if word1 not in uniqueState:
            uniqueState[word1] = stateCounter
            stateCounter += 1
        if word2 not in uniqueState:
            uniqueState[word2] = stateCounter
            stateCounter += 1

        # collect frequency
        if word1 in bigramProb:
            if word2 in bigramProb[word1]:
                bigramProb[word1][word2] += 1
            else:
                bigramProb[word1][word2] = 1
        else:
            bigramProb[word1] = {}
            bigramProb[word1][word2] = 1


# convert frequency to probability
# unigram
total = 0
for word,freq in unigramProb.items():
    total += freq

for word,freq in unigramProb.items():
    unigramProb[word] = freq/total

# bigram
for word1, innerDict in bigramProb.items():
    total = 0
    for word2, freq in innerDict.items():
        total += freq

    for word2, freq in innerDict.items():
        bigramProb[word1][word2] = freq/total

# writing a wfsa
outFile.write('END\n')

# add unigram probabilities to the wfsa
for word, prob in unigramProb.items():
    targetState = uniqueState[word]
    outFile.write('(START ('+str(targetState)+' "'+word+'" '+str(prob)+'))\n')

# add bigram probabilities to the wfsa
for word1, innerDict in bigramProb.items():
    for word2, prob in innerDict.items():
        
        if word2 is not 'END':
            startState = uniqueState[word1]
            targetState = uniqueState[word2]
            outFile.write('('+str(startState)+' ('+str(targetState)+' "'+word2+'" '+str(prob)+'))\n')
        else:
            startState = uniqueState[word1]
            targetState = 'END'
            outFile.write('('+str(startState)+' ('+targetState+' "'+word2+'" '+str(prob)+'))\n')

outFile.close()
