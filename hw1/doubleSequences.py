inpFile = open('/home/student/cs662/hw1/spanishvocab.txt', 'r')

dictio = {}

for line in inpFile:
    line = line.strip()
    line = line.replace(' ', '')
    for pos in range(len(line)-1):
        seq = line[pos:pos+2]
        if seq not in dictio:
            dictio[seq] = 1
        else:
            dictio[seq] = dictio[seq]+1

print(dictio)
