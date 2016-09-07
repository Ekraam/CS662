import subprocess

inpFile = open('/home/student/cs662/hw1/spanishvocab.txt', 'r')

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
    output = subprocess.check_output(command, shell=True)

    if output.count('\n')!=2:
        print('String not accepted - '+word)
