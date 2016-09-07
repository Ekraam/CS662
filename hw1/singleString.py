import subprocess
import os

inpFile = open('/home/student/cs662/hw1/spanishvocab.txt', 'r')

singleString = ''

count = 0

for line in inpFile:
    if count<1000:
        count += 1
        for char in line:
            if char != ' ' and char != '\n':
                singleString += '"'+char+'" '
                singleString += '"_" '
                
singleString = singleString[:len(singleString)-5]
inpFile.close()

command = 'echo \''+singleString+'\' | /home/student/graehl/carmel/bin/carmel -sliO spanish.fsa > output.txt'

subprocess.check_output(command, shell=True)
#os.system(command)
