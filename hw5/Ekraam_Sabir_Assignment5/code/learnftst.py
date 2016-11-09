from __future__ import division
from collections import Counter

# read the files

treeFile = open("hw5.train.trees", 'r')
engFile = open("./hw5.train.strings", 'r')
spanFile = open("./hw5.train.strings.spa", 'r')
alignFile = open('hw5.alignments', 'r')
outFile = open('eng-spa.tt', 'w')

treeStrings = treeFile.readlines()
engStrings = engFile.readlines()
spanStrings = spanFile.readlines()
alignments = alignFile.readlines()

# uncomment to extract rules only from first 1 sentence
'''
treeStrings = treeStrings[:1]
engStrings = engStrings[:1]
spanStrings = spanStrings[:1]
alignments = alignments[:1]
'''

terminalProb = {}
wordBank = []

# learn terminal rules

for i in range(len(engStrings)):
    
    engTokens = (engStrings[i].strip()).split()
    spanTokens = (spanStrings[i].strip()).split()
    alignLinks = (alignments[i].strip()).split()

    # create buffer of positions
    buffer = []
    for word in engTokens:
        buffer.extend([word])
    multBuffer = []
    for links in alignLinks:
        pos = links.split('-')
        multBuffer.extend([ engTokens[int(pos[1])] ])
    duplicateBuffer = [k for k,v in Counter(multBuffer).items() if v>1]
    buffer = list(set(buffer))
    tempStorage = {}

    # collect counts
    for link in alignLinks:
        
        pos = link.split('-')
        spanPos = int(pos[0])
        engPos = int(pos[1])

        engWord = engTokens[engPos]
        spanWord = spanTokens[spanPos]

        if engWord in buffer:
            buffer.remove(engWord)

        if engWord in duplicateBuffer:

            if engWord in tempStorage:
                tempStorage[engWord] += ' '+spanWord
            else:
                tempStorage[engWord] = spanWord
        else:
            if engWord in terminalProb:
                if spanWord in terminalProb[engWord]:
                    terminalProb[engWord][spanWord] += 1
                else:
                    terminalProb[engWord][spanWord] = 1
            else:
                terminalProb[engWord] = {}
                terminalProb[engWord][spanWord] = 1
                wordBank.extend([engWord])

    # add multiple aligned rules
    for engWord, spanPhrase in tempStorage.items():
        if engWord in terminalProb:
            if spanPhrase in terminalProb[engWord]:
                terminalProb[engWord][spanPhrase] += 1
            else:
                terminalProb[engWord][spanPhrase] = 1
        else:
            terminalProb[engWord] = {}
            terminalProb[engWord][spanPhrase] = 1

    # add empty engwords with no links
    for engWord in buffer:

        if engWord in terminalProb:
            if '*e*' in terminalProb[engWord]:
                terminalProb[engWord]['*e*'] += 1
            else:
                terminalProb[engWord]['*e*'] = 1
        else:
            terminalProb[engWord] = {}
            terminalProb[engWord]['*e*'] = 1
            wordBank.extend([engWord])

# 5 most commonly seen rules
countList = []
for engWord, dictionary in terminalProb.items():
    for spanWord, count in dictionary.items():
        countList.extend([count])

# Learn tree rules
stateProb = {}
rootBank = ['TOP']

def processSubtree(subString):

    if subString.find('(')<0:
        print 'invalid subString given'
    
    pos = subString.find('(')
    child = subString[:pos]
    count = 0
    idx = pos
    remainString = ''
    startString = ''
    for char in subString[pos:]:
        if char=='(':
            count += 1
        elif char==')':
            count -= 1
        if count==0:
            remainString = subString[idx+1:]
            startString = subString[:idx+1]
            break
        idx += 1
            
    remainString = remainString.strip()
    startString = startString.strip()

    singleTreeRule(startString)

    return [child, remainString]

def singleTreeRule(tree):

    global stateProb
    global rootBank

    if tree.find('(')>-1:
        
        rootWord = tree[:tree.find('(')]
        midString = tree[tree.find('(')+1:tree.rfind(')')]
        rootBank.extend([rootWord])
        rootBank = list(set(rootBank))
        
        if midString.find('(')>-1:
            children = ''
            while len(midString)>0:
                buffer = processSubtree(midString)
                children += buffer[0]+' '
                midString = buffer[1]
        else:
            children = midString

        # update rule to the dictionary
        children = children.strip()
        if rootWord in stateProb:
            if children in stateProb[rootWord]:
                stateProb[rootWord][children] += 1
            else:
                stateProb[rootWord][children] = 1
        else:
            stateProb[rootWord] = {}
            stateProb[rootWord][children] = 1

# process all trees to extract rules
for tree in treeStrings:
    
    tree = tree.strip()
    #print 'Processing tree: '+tree
    singleTreeRule(tree)

# 5 most freq count processing
for rootWord, dictionary in stateProb.items():
    for children, count in dictionary.items():
        countList.extend([count])

countList.sort()
countList.reverse()
top5List = countList[:6]
top5Dict = {}
for count in top5List:
    top5Dict[count] = ''

for engWord, dictionary in terminalProb.items():
    for spanWord, count in dictionary.items():
        if count in top5Dict:
            top5Dict[count] = engWord+' - '+spanWord

for rootWord, dictionary in stateProb.items():
    for children, count in dictionary.items():
        if count in top5Dict:
            top5Dict[count] = rootWord+' - '+children
print 'Top 5 rules with count'
print top5Dict

# convert count to prob
for engWord, val in terminalProb.items():
    count = 0
    for spanWord, freq in val.items():
        count += freq
        
    for spanWord, freq in val.items():
        terminalProb[engWord][spanWord] = freq/count

# convert state freq to probability
for root, childDict in stateProb.items():
    count = 0
    for children, freq in childDict.items():
        count += freq

    for children, freq in childDict.items():
        stateProb[root][children] = freq/count

# print the rules in wftst file
outFile.write('q\n')
middle = ' -> '
for root, dictionary in stateProb.items():
    for children, prob in dictionary.items():
        childList = children.split()
        
        # left hand side of rule
        LHS = 'q.'+root+'('
        for idx in range(len(childList)):
                LHS += 'x'+str(idx)+':'+childList[idx]+' '
        LHS = LHS.strip()
        LHS += ')'

        # right hand side of rule
        RHS = ''
        for idx in range(len(childList)):
            if childList[idx] in rootBank:
                RHS += 'q.x'+str(idx)+' '
            else:
                RHS += 't.x'+str(idx)+' '
        RHS = RHS.strip()
        RHS += ' # '+str(prob)
        
        outFile.write(LHS+middle+RHS+'\n')

for engWord, spanDict in terminalProb.items():
    for spanWord, prob in spanDict.items():
        rule = 't.'+engWord+' -> '+spanWord+' # '+str(prob)+'\n'
        outFile.write(rule)

outFile.close()
engFile.close()
spanFile.close()
treeFile.close()
alignFile.close()
