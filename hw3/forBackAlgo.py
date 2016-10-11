# this code uses the forward-backward implementation
# for decipherment

from __future__ import division
import math

engData = open('./english.data', 'r')
engLines = engData.readlines()

bigramProb = {}
bigramFreq = {}
unigramProb = {}

charlist = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ '

# unigram probability
for char in charlist:
    unigramProb[char] = math.log(1/len(charlist))

# bigram probabilities
for char in charlist:
    
    bigramProb[char] = {}
    bigramFreq[char] = {}

    for char2 in charlist:
        bigramProb[char][char2] = 0
        bigramFreq[char][char2] = 0

for i in range(len(engLines)):
    
    line = engLines[i]
    line = line.strip()
    line = ' '+line+' '
    
    for j in range(0,len(line)-1):
        char1 = line[j]
        char2 = line[j+1]
        bigramFreq[char1][char2] += 1

for char1, target in bigramFreq.items():
    totalCount = 0
    for char2, count in target.items():
        totalCount += count
        
    for char2, count in target.items():
        if count/totalCount!=0:
            bigramProb[char1][char2] = math.log(count/totalCount)
        else:
            bigramProb[char1][char2] = -1e+200
        
# EM section with forward backward

channelProb = {}

for char in charlist:
    
    channelProb[char] = {}
    for char2 in charlist:
        if char!=' ' and char2!=' ':
            channelProb[char][char2] = math.log(1/26)
        elif char==' ' and char2==' ':
            channelProb[char][char2] = math.log(1)
        else:
            channelProb[char][char2] = -1e+200

countCollection = {}
for char in charlist:
    countCollection[char] = {}
    for char2 in charlist:
        countCollection[char][char2] = 0

def add(logx, logy):
    if logx<=-100:
        return logy
    if logy<=-100:
        return logx
    if (logx-logy)>16:
        return logx
    if logx>logy:
        return logx+math.log(1+math.exp(logy-logx))
    if (logy-logx)>16:
        return logy
    if logy>logx:
        return logy+math.log(1+math.exp(logx-logy))

inpFile = open('./cipher.data', 'r')
inpLine = inpFile.readlines()
inpLine = inpLine[0]
inpLine = inpLine.strip()
inpLine = 'MTBS SQTVTCEQZV TDSTNESM TX BZOZ WSQVEGS XTQJM TG TDS ITNMSGEGC ZCNEQJVTJNZV ZGW NSMTJNQS QTGWETETGM EG TDS VZTS QVZMMEQ YSNETW ET IZM TNECEGZVVO TDTJCDT TDZT TDS BZRTNETO TX BZOZ ZCNEQJVTJNS IZM WSYSGWSGT TG Z MEBYVS MVZMDZGWAJNG'
inpFile.close()
lenLine = len(inpLine)
Cols = lenLine*2
Rows = 27

for iter in range(5):

    alphaMatrix = [[-1e+200 for y in range(Cols)] for x in range(Rows)]
    betaMatrix = [[-1+200 for y in range(Cols)] for x in range(Rows)]
    alphaFinalState = -1e+200

    # calculate alpha
    for col in range(Cols):
        for row in range(Rows):

            echar = charlist[row]

            if col==0:
                alphaMatrix[row][col] = unigramProb[echar]
            elif col%2==0:
                for prevRow in range(Rows):
                    echarPrev = charlist[prevRow]
                    alphaMatrix[row][col] = add(alphaMatrix[prevRow][col-1]+bigramProb[echarPrev][echar], alphaMatrix[row][col]) # += multiplication
            else:
                cchar = inpLine[col//2]
                alphaMatrix[row][col] = alphaMatrix[row][col-1]+channelProb[echar][cchar] # multiplication

    for row in range(Rows):
        alphaFinalState = add(alphaMatrix[row][Cols-1],alphaFinalState)
        #alphaFinalState += alphaMatrix[row][Cols-1]

    # calculate beta
    for col in range(Cols-1, -1, -1):
        for row in range(Rows):
            
            echar = charlist[row]

            if col==(Cols-1):
                betaMatrix[row][col] = 1
            elif col%2!=0:
                for nextRow in range(Rows):
                    echarNext = charlist[nextRow]
                    betaMatrix[row][col] += betaMatrix[nextRow][col+1]*bigramProb[echar][echarNext]
            else:
                cchar = inpLine[col//2]
                betaMatrix[row][col] = betaMatrix[row][col+1]*channelProb[echar][cchar]

    # count collection
    for row in range(Rows):
        echar = charlist[row]

        for col in range(0,Cols,2):            
            cchar = inpLine[col//2]
            countCollection[echar][cchar] += (alphaMatrix[row][col]*channelProb[echar][cchar]*betaMatrix[row][col+1])/alphaFinalState

    # count normalization
    for echar, ccharDict in countCollection.items():
        total = 0
        for cchar, count in ccharDict.items():
            total += count
        for cchar, count in ccharDict.items():
            channelProb[echar][cchar] = count/total
            countCollection[echar][cchar] = 0

    # viterbi and forward
    Q = [[0 for x in range(Cols//2)] for y in range(Rows)] 
    best_pred = [[0 for x in range(Cols//2)] for y in range(Rows)] 
    alpha = [[0 for x in range(Cols//2)] for y in range(Rows)] 

    for row in range(Rows):
        echar = charlist[row]
        cchar = inpLine[0]
        Q[row][0] = unigramProb[echar]*channelProb[echar][cchar]
        alpha[row][0] = unigramProb[echar]*channelProb[echar][cchar]

    for col in range(1,Cols//2):
        cchar = inpLine[col]

        for row in range(Rows):
            echar = charlist[row]
            Q[row][col] = 0
            best_pred[row][col] = 0
            best_score = -1
            
            for k in range(Rows):
                ccharPrev = charlist[k]
                r = bigramProb[ccharPrev][echar]*channelProb[echar][cchar]*Q[k][col-1]
                alpha[row][col] += bigramProb[ccharPrev][echar]*channelProb[echar][cchar]*alpha[k][col-1]
                if r>best_score:
                    best_score = r
                    best_pred[row][col] = k
                    Q[row][col] = r

    final_best = 0
    final_score = -1
    for row in range(Rows):
        if Q[row][(Cols//2)-1] > final_score:
            final_score = Q[row][(Cols//2)-1]
            final_best = row

    decipherText = [charlist[row]]
    current = final_best
    for col in range((Cols//2)-1, 0, -1):
        current = best_pred[current][col]
        decipherText.extend([charlist[current]])

    decipherText.reverse()

    Pcipher = 0
    for row in range(Rows):
        Pcipher += alpha[row][(Cols//2)-1]

    print('EM iteration '+str(iter+1))
    print('P(cipher) '+str(Pcipher))
    print(decipherText)
    
