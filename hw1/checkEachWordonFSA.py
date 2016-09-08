import subprocess
import commands

inpFile = open('/home/student/cs662/hw1/spanishvocab.txt', 'r')

stringReject = {}
rightSeq = 0

for line in inpFile:
    line = line.strip()
    if line == '':
        print('Blank encountered')
    
    line = line.replace(' ', '')
    word = '\' '
    for char in line:
        word = word+'"'+char+'" '
    word = word+'\''

    command = 'echo '+word+' | /home/student/graehl/carmel/bin/carmel -sli spanish.fsa > output.txt'
    #output = subprocess.check_output(command, stderr=subprocess.STDOUT)
    output = commands.getstatusoutput(command)
    if output[1].find('invalid')>=0:
        print('String not accepted: '+line)
        stringReject[line] = 1
    else:
        rightSeq += 1
        print(rightSeq)

inpFile.close()
print(stringReject)
