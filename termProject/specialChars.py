# this script will find the non alphabetic characters in a file

inpFile = open('./translation.raw', 'r')

specialSet = set()

for line in inpFile:
    line = line.strip()
    for char in line:
        if not char.isalpha():
            specialSet.add(char)

print 'The non alphabetic characters in file are '
print specialSet
