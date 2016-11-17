import requests

playNames = ['antony-and-cleopatra', 'asyoulikeit', 'errors', 'hamlet', 'henry4pt1', 'henry4pt2', 'henryv', 'juliuscaesar', 'lear', 'macbeth', 'merchant', 'msnd', 'muchado', 'othello', 'richardiii', 'romeojuliet', 'shrew', 'tempest', 'twelfthnight']
pageRange = ['2-352', '2-242', '2-162', '2-336', '3-255', '269-537', '2-276', '2-238', '2-310', '2-218', '2-230', '2-180', '2-238', '2-306', '2-342', '4-286', '2-248', '2-202', '2-242']

rawShakespeare = open('shakespeare.raw', 'w')
rawTranslation = open('translation.raw', 'w')

endDelimiter = '</div>'

for play in playNames:

    print ('Reading play: '+play)
    rawShakespeare.write('--%%-- Play: '+play+' --%%--\n \n')
    rawTranslation.write('--%%-- Play: '+play+' --%%--\n \n')

    startPage = int(pageRange[playNames.index(play)].split('-')[0])
    endPage = int(pageRange[playNames.index(play)].split('-')[1]) 

    for page in range(startPage, endPage+1, 2):
        
        print ('page number: '+str(page))
        rawShakespeare.write('--%%-- pageNum: '+str(page)+' --%%--\n \n')
        rawTranslation.write('--%%-- pageNum: '+str(page)+' --%%--\n \n')
        
        # read page into temporary file
        tempPage = open('./tempPage.txt', 'w')
        response = requests.get('http://nfs.sparknotes.com/'+play+'/page_'+str(page)+'.html')
        tempPage.write(response.content)
        tempPage.close()

        # extract relevant lines into single file for all plays
        tempPage = open('./tempPage.txt', 'r')
        tempLines = tempPage.readlines()
        tempPage.close()

        i = 0
        while i<len(tempLines):
            line = tempLines[i]
            if line.find("original-line")>=0:

                # get range of shakespeare lines
                counter = i

                while tempLines[counter].find('modern-line')<0:
                    counter += 1
                counter -= 1

                if tempLines[counter].find('</div>')<0:
                    while tempLines[counter].find('</div>')<0:
                        counter -= 1
                else:
                    counter -= 2

                # extract the shakespeare lines
                shakespeareLine = ''
                for idx in range(i, counter+1):
                    startPos = tempLines[idx].find('original-line')
                    if startPos>=0:
                        shakespeareLine += tempLines[idx][startPos+15:].strip() + ' '
                    else:
                        shakespeareLine += tempLines[idx].strip() + ' '

                # get range of translation lines
                counter += 1
                while tempLines[counter].find('modern-line')<0:
                    counter += 1
                endPos = counter
                while tempLines[endPos].find(endDelimiter)<0:
                    endPos += 1

                # extract translation lines
                translationLine = ''
                for idx in range(counter, endPos+1):
                    startPos = tempLines[idx].find('modern-line')
                    if startPos>=0:
                        translationLine += tempLines[idx][startPos+13:].strip() + ' '
                    else:
                        translationLine += tempLines[idx].strip() + ' '

                # all processing on the extracted lines here
                shakespeareLine = shakespeareLine.replace(endDelimiter, '')
                translationLine = translationLine.replace(endDelimiter, '')
                shakespeareLine = shakespeareLine.replace('&nbsp;', '')
                translationLine = translationLine.replace('&nbsp;', '')
                shakespeareLine = shakespeareLine.replace('&ldquo;', '"')
                translationLine = translationLine.replace('&ldquo;', '"')
                shakespeareLine = shakespeareLine.replace('&rsquo;', '\'')
                translationLine = translationLine.replace('&rsquo;', '\'')
                shakespeareLine = shakespeareLine.replace('&rdquo;', '"')
                translationLine = translationLine.replace('&rdquo;', '"')
                shakespeareLine = shakespeareLine.replace('&mdash;', '-')
                translationLine = translationLine.replace('&mdash;', '-')
                shakespeareLine = shakespeareLine.replace('&egrave;', 'e')
                translationLine = translationLine.replace('&egrave;', 'e')
                shakespeareLine = shakespeareLine.replace('&aelig;', 'ae')
                translationLine = translationLine.replace('&aelig;', 'ae')
                shakespeareLine = shakespeareLine.replace('&lsquo;', '\'')
                translationLine = translationLine.replace('&lsquo;', '\'')
                shakespeareLine = shakespeareLine.replace('&eacute;', 'e')
                translationLine = translationLine.replace('&eacute;', 'e')
                shakespeareLine = shakespeareLine.replace('&ndash;', '-')
                translationLine = translationLine.replace('&ndash;', '-')
                shakespeareLine = shakespeareLine.replace('&emsp;', '')
                translationLine = translationLine.replace('&emsp;', '')
                shakespeareLine = shakespeareLine.replace('&agrave;', 'a')
                translationLine = translationLine.replace('&agrave;', 'a')
                shakespeareLine = shakespeareLine.replace('&hellip;', '...')
                translationLine = translationLine.replace('&hellip;', '...')
                shakespeareLine = shakespeareLine.replace('&Ocirc;', 'O')
                translationLine = translationLine.replace('&Ocirc;', 'O')
                shakespeareLine = shakespeareLine.replace('&acirc;', 'a')
                translationLine = translationLine.replace('&acirc;', 'a')
                shakespeareLine = shakespeareLine.replace('&ccedil;', 'c')
                translationLine = translationLine.replace('&ccedil;', 'c')
                shakespeareLine = shakespeareLine.replace('&ecirc;', 'e')
                translationLine = translationLine.replace('&ecirc;', 'e')
                shakespeareLine = shakespeareLine.replace('&icirc;', 'i')
                translationLine = translationLine.replace('&icirc;', 'i')
                shakespeareLine = shakespeareLine.replace('&gt;', '>')
                translationLine = translationLine.replace('&gt;', '>')
                shakespeareLine = shakespeareLine.replace('&amp;', '&')
                translationLine = translationLine.replace('&amp;', '&')
                shakespeareLine = shakespeareLine.replace('&iuml;', 'i')
                translationLine = translationLine.replace('&iuml;', 'i')
                shakespeareLine = shakespeareLine.replace('&sbquo;', '')
                translationLine = translationLine.replace('&sbquo;', '')
                shakespeareLine = shakespeareLine.replace('\n', '')
                translationLine = translationLine.replace('\n', '')
                shakespeareLine = shakespeareLine.strip()
                translationLine = translationLine.strip()

                # write the lines to respective files
                rawShakespeare.write(shakespeareLine+'\n \n')
                rawTranslation.write(translationLine+'\n \n')

                # jump value of i to get past this set of sentences
                i = endPos
                
            else:
                i += 1





rawShakespeare.close()
rawTranslation.close()
