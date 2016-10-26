# This script learns the grammar rules from the trees

from __future__ import division
import fileinput
import pickle

outFile = open('./train.trees.pre.unk.rules', 'w')

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
                grammar[label][terms] = 1
        else:
            grammar[label] = {}
            grammar[label][terms] = 1
            
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

pickle.dump(grammar, open('grammar.pkl', 'wb'))
pickle.dump(list(set(wordList)), open('wordList.pkl', 'wb'))
pickle.dump(list(set(N)), open('N.pkl', 'wb'))
