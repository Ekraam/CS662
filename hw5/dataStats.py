from __future__ import division

# read the files

engFile = open("./hw5.train.strings", 'r')
spanFile = open("./hw5.train.strings.spa", 'r')
alignFile = open('hw5.alignments', 'r')

engStrings = engFile.readlines()
spanStrings = spanFile.readlines()
alignments = alignFile.readlines()

# check for equal lines
if len(engStrings)!=len(spanStrings) or len(spanStrings)!=len(alignments):
    print('Files have unequal number of lines')

# count english words
engCount = 0
for line in engStrings:
    line = line.strip()
    line = line.split()
    engCount += len(line)

print 'number of english tokens '+str(engCount)

# count spanish words
spanCount = 0
for line in spanStrings:
    line = line.strip()
    line = line.split()
    spanCount += len(line)

print 'number of spanish tokens '+str(spanCount)

# count links and aligned english tokens
linkCount = 0
engLinkCount = 0
for line in alignments:
    line = line.strip()
    line = line.split()
    linkCount += len(line)
    engNums = []

    for links in line:
        engNums.extend([links.split('-')[1]])
    engLinkCount += len(set(engNums))

unalignEngTokens = 100*(engCount - engLinkCount)/engCount

print 'number of links '+str(linkCount)
print 'number of unaligned english tokens '+str(engCount-engLinkCount)
print '% of unaligned english tokens '+str(unalignEngTokens)
