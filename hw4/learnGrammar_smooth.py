# This script learns the grammar rules from the trees

from __future__ import division
import fileinput
import pickle

outFile = open('./train.trees.pre.unk.rules_smooth', 'w')

grammar = {}
wordList = []
N = []

def parseTree(Line):

    global wordList
    global grammar
    global N

    # Non terminal term
    if Line.count('(')>=2:
        Line = Line[1:]
        Line = Line[:len(Line)-1]
        label = Line[:Line.find(' ')+1]
        label = label.strip()
        N.extend([label])
        Line = Line[Line.find('('):]
        counter = 0
        pos = 0
        midPoint = -1
        # find mid space to divide line
        for char in Line:
            if char=='(':
                counter += 1
            elif char==')':
                counter -= 1
            else:
                pos += 1
                continue
            if counter==0:
                midPoint = pos
                break
            pos += 1

        if midPoint==-1:
            print('No midPoint found')
            
        # divide the line and get the terms
        line1 = Line[:midPoint+1]
        line2 = Line[midPoint+2:]
        terms = parseTree(line1)
        terms = terms.strip()
        terms = terms+' '+parseTree(line2).strip()
                
        # add to grammar
        if label in grammar:
            if terms in grammar:
                grammar[label][terms] += 1
            else:
                grammar[label][terms] = 1 # to keep it > smoothened prob
        else:
            grammar[label] = {}
            grammar[label][terms] = 1 # to keep it > smoothened prob
            
        # return
        if 'TOP' in label:
            return 1
        else:
            return label

    # terminal term
    else:
        Line = Line[1:]
        Line = Line[:len(Line)-1]
        terms = Line.split()

        # add count in dictionary
        label = terms[0]
        label = label.strip()
        word  = terms[1]
        word = word.strip()
        wordList.extend([word])
        N.extend([label])
        if label in grammar:
            if word in grammar[label]:
                grammar[label][word] += 1
            else:
                grammar[label][word] = 1
        else:
            grammar[label] = {}
            grammar[label][word] = 1
        return label

# process all trees        
for line in fileinput.input():
    line = line.strip()
    parseTree(line)

# make the lists have unique elements
N = list(set(N))
wordList = list(set(wordList))

# add one smoothing (allow every rule to be possible with very little probability)
print('Starting add 1 smoothing will take couple of minutes')

# labels to 2 terms (non terminal rules)
for label, dictionary in grammar.items():
    for label1 in N:
        if label1 is not 'TOP':
            for label2 in N:
                if label2 is not 'TOP':
                    term = label1+' '+label2
                    if term not in dictionary.keys():
                        grammar[label][term] = 1e-10
print('2 term smoothing done')

# labels to 1 term/word (terminal rules)
for label, dictionary in grammar.items():
    if label is 'SYM':
        for word in wordList:
            if word not in dictionary.keys() and len(word)==1:
                grammar[label][word] = 1e-10
print('1 term smoothing done')

# convert to probability
maxCount = 0
maxLabel = ''
maxTerms = ''
for label, dictionary in grammar.items():
    count = 0
    for terms, freq in grammar[label].items():
        count += freq
        if freq>maxCount:
            maxCount = freq
            maxLabel = label
            maxTerms = terms

    for terms, freq in grammar[label].items():
        prob = freq/count
        grammar[label][terms] = prob
        
# write the rules to a file
for label, dictionary in grammar.items():
    for terms, prob in grammar[label].items():
        outFile.write(label.strip()+' -> '+' '.join(terms.split())+' # '+str(prob)+'\n')

outFile.close()

print('Most frequent rule is '+maxLabel+' -> '+maxTerms+' with a frequency of '+str(maxCount))

pickle.dump(grammar, open('grammar_smooth.pkl', 'wb'))
pickle.dump(wordList, open('wordList_smooth.pkl', 'wb'))
pickle.dump(N, open('N_smooth.pkl', 'wb'))
