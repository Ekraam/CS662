# This code implements the viterbi CMYK algorithm
# to get the best parse for a sentence

import pickle
import math
import time
import matplotlib.pyplot as plt

grammar = pickle.load(open('./grammar.pkl', 'rb'))
wordList = pickle.load(open('./wordList.pkl', 'rb'))
N = pickle.load(open('./N.pkl', 'rb'))

inpFile = open('./test.strings', 'r')
outFile = open('./test.parses', 'w')

best = {}
back = {}

def viterbi(line):

    global best
    global back

    back={}
    best={}
    
    line = line.split()

    # replace unseen words with <unk>
    for i in range(0,len(line)):
        word = line[i]
        if word not in wordList:
            line[i] = '<unk>'

    # initialize
    firstPass = True
    for j in range(1,len(line)+1):
        for i in range(0,j):
            if i not in best.keys():
                best[i] = {}
                back[i] = {}
            best[i][j] = {}
            back[i][j] = {}
            for label in N:
                best[i][j][label] = float('-inf')
                back[i][j][label] = []

    # initialize diagonal
    for i in range(1,len(line)+1):
        wi = line[i-1]
        for X, dictionary in grammar.items():
            for YZ, prob in dictionary.items():
                if YZ==wi and math.log10(prob)>best[i-1][i][X]:
                    best[i-1][i][X] = math.log10(prob)
                    back[i-1][i][X] = [i-1, i, YZ]

    # final loop set
    for l in range(2,len(line)+1):
        for i in range(0, len(line)-l+1):
            j = i+l
            for k in range(i+1, j):

                # for all YZ
                for Y in N:
                    for Z in N:
                        YZ = Y+' '+Z
                        
                        # if it's a valid rule
                        for X, dictionary in grammar.items():
                            for key, prob in dictionary.items():
                                if key==YZ and math.log10(prob)+best[i][k][Y]+best[k][j][Z]>best[i][j][X]:
                                    best[i][j][X] = math.log10(prob)+best[i][k][Y]+best[k][j][Z]
                                    back[i][j][X] = [i, k, Y, k, j, Z]

# function to extract the prased tree
def conv2Tree(i, j, X):
    
    data = back[i][j][X]
    if len(data)==6:
        k = data[1]
        Y = data[2]
        Z = data[5]
        sub1 = conv2Tree(i, k, Y)
        sub2 = conv2Tree(k, j, Z)
        tree = '('+X+' '+sub1+' '+sub2+')'
        return tree
    else:
        YZ = back[i][j][X][2]
        tree = '('+X+' '+YZ+')'
        return tree

# loop to process input string
logTime = []
logLength = []
for line in inpFile:
    line = line.strip()
    print(line)
    start = time.time()
    viterbi(line)
    end = time.time()

    line = line.split()

    logTime.extend([math.log10(end-start)])
    logLength.extend([math.log10(len(line))])

    if len(back[0][len(line)]['TOP'])>0:
        tree = conv2Tree(0, len(line), 'TOP')
        outFile.write(tree+'\n')
        print('log(time) '+str(math.log10(end-start))+' log(length) '+str(math.log10(len(line)))+' log(prob) '+str(best[0][len(line)]['TOP']))
    else:
        # making probability -inf since a full path was not found
        print('log(time) '+str(math.log10(end-start))+' log(length) '+str(math.log10(len(line)))+' log(prob) -inf ')

        print('partial output on this one')
        # get best element in 0 row
        bestProb = float('-inf')
        colpos = 0
        collabel = ''
        leave = False
        for j in range(len(line), 0, -1):
            for key,val in back[0][j].items():
                if len(val)>0:
                    if best[0][j][key]>bestProb:
                        colpos = j
                        collabel = key
                        bestProb = best[0][j][key]
                        leave = True
            if leave:
                break
        line1 = conv2Tree(0, colpos, collabel)
        
        # get best element in last col
        bestProb = float('-inf')
        rowpos = 0
        rowlabel = ''
        leave = False
        for i in range(0, len(line)):
            for key,val in back[i][len(line)].items():
                if len(val)>0:
                    if best[i][len(line)][key]>bestProb:
                        rowpos = i
                        rowlabel = key
                        bestProb = best[i][len(line)][key]
                        leave = True
            if leave:
                break
        line2 = conv2Tree(rowpos, len(line), rowlabel)

        outFile.write('(TOP '+line1+' '+line2+')\n')

inpFile.close()
outFile.close()

plt.plot(logLength, logTime)
plt.xlabel('log(length)')
plt.ylabel('log(time)')
plt.grid(True)
plt.show()
