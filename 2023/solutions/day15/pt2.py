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

def findIndex(list, func):
    for i in range(0, len(list)):
        if func(list[i]):
            return i
    return -1
        
box_map = {}
for i in range(0, 256):
    box_map[i] = []

for step in seq:
    step = step.strip()

    if "=" in step:
        parts = step.split("=")
        label = parts[0]
        box_num = hash(label)
        focal_length = int(parts[1])

        print(f'{label}: {focal_length}')

        lenses = box_map[box_num]
        idx = findIndex(lenses, lambda item: item[0] == label)
        if idx >= 0:
            lenses[idx] = (label, focal_length)
        else:
            lenses.append((label, focal_length))

    else:
        label = step.split("-")[0]
        box_num = hash(label)

        print(label)
        lenses = box_map[box_num]
        idx = findIndex(lenses, lambda item: item[0] == label)
        if idx >= 0:
            lenses.pop(idx)
        

for key in box_map:
    lenses = box_map[key]
    if len(lenses) > 0:
        print(f'Box {key}: {lenses}')

total_power = 0

for box_num in box_map:
    lenses = box_map[box_num]
    for i in range(0, len(lenses)):
        power = (box_num+1) * (i+1) * lenses[i][1]
        print(f'Power: {power}')
        total_power += power

print(f'Total power: {total_power}')