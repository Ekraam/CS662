from __future__ import division

# read the files

treeFile = open("hw5.train.trees", 'r')
engFile = open("./hw5.train.strings", 'r')
spanFile = open("./hw5.train.strings.spa", 'r')
alignFile = open('hw5.alignments', 'r')

treeStrings = treeFile.readlines()
engStrings = engFile.readlines()
spanStrings = spanFile.readlines()
alignments = alignFile.readlines()

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
    buffer = list(set(buffer))

    # collect counts
    for link in alignLinks:
        
        pos = link.split('-')
        spanPos = int(pos[0])
        engPos = int(pos[1])

        engWord = engTokens[engPos]
        spanWord = spanTokens[spanPos]
        if engWord in buffer:
            buffer.remove(engWord)

        if engWord in terminalProb:
            if spanWord in terminalProb[engWord]:
                terminalProb[engWord][spanWord] += 1
            else:
                terminalProb[engWord][spanWord] = 1
        else:
            terminalProb[engWord] = {}
            terminalProb[engWord][spanWord] = 1
            wordBank.extend([engWord])

    # add empty engwords with no links
    for engWord in buffer:
        print 'unlinked word '+engWord+' found'

        if engWord in terminalProb:
            if '*e*' in terminalProb[engWord]:
                terminalProb[engWord]['*e*'] += 1
            else:
                terminalProb[engWord]['*e*'] = 1
        else:
            terminalProb[engWord] = {}
            terminalProb[engWord]['*e*'] = 1
            wordBank.extend([engWord])

            
# convert count to prob
for engWord, val in terminalProb.items():
    count = 0
    for spanWord, freq in val.items():
        count += freq
        
    for spanWord, freq in val.items():
        terminalProb[engWord][spanWord] = freq/count

# Learn tree rules
stateProb = {}
rootBank = ['TOP']

def processSubtree(subString):

    if subString.find('(')<0:
        print 'invalid subString given'
    
    pos = subString.find('(')
    child = subString[:pos]
    print 'child '+child
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
    print 'remainString '+remainString
    print 'startString '+startString
    singleTreeRule(startString)

    return [child, remainString]

def singleTreeRule(tree):

    global stateProb
    global rootBank

    if tree.find('(')>-1:
        
        rootWord = tree[:tree.find('(')]
        midString = tree[tree.find('(')+1:tree.rfind(')')]
        
        if midString.find('(')>-1:
            children = ''
            while len(midString)>0:
                buffer = processSubtree(midString)
                print buffer
                children += buffer[0]+' '
                midString = buffer[1]
                rootBank.extend([children.strip()])
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

for tree in treeStrings:
    
    tree = tree.strip()
    print 'processing tree '+tree
    singleTreeRule(tree)

