inpFile = open('/home/student/cs662/hw1/spanishvocab.txt', 'r')
length = 0

for line in inpFile:
    if length<len(line):
        length = len(line)
    if len(line)==45:
        print(line)

print(length)

inpFile.close()
