import re

inputFile = open('input.txt', 'r')
seq = []

# Read lines
while True:
    line = inputFile.readline()
    if not line:
        break

    seq += re.split(',', line)

inputFile.close()

def hash(str):
    val = 0

    for char in str:
        val += ord(char)
        val *= 17
        val = val % 256

    return val
    
        
totals = 0

for str in seq:
    totals += hash(str.strip())

print(f'Total: {totals}')