import re
import sys
sys.setrecursionlimit(1000000)

inputFile = open('input.txt', 'r')
lines = []
DIRS = ['R', 'D', 'L', 'U']

# Read lines
while True:
    line = inputFile.readline()
    if not line:
        break

    match = re.match(r'([A-Z]) ([0-9]+) \((.*)\)', line)

    # Split "color" token into 5 digits & 1 digit at end (direction)
    token = match[3]
    count_raw = token[1:6]
    dir_raw = token[6:]

    # Convert from base 16
    count = int(count_raw, 16)

    # Map to DIR char
    dir = DIRS[int(dir_raw)]

    lines.append((dir, count))

inputFile.close()


# Build "point" coordinates for polygon representing the trench shape.
trench = [(0, 0)]
trench_length = 0
posX = 0
posY = 0

for line in lines:
    (dir, count) = line

    if dir == 'R': posX += count
    if dir == 'L': posX -= count
    if dir == 'D': posY += count
    if dir == 'U': posY -= count

    trench.append((posX, posY))
    trench_length += count

# Shoelace algorithm to compute area of 2D polygon give ordered list of point coordinates.
def shoelace(path: list):
    # Add first item to back of list for our shoelace loop algo.
    padded = path.copy()
    padded.append(path[0])

    # Lace em up
    area = 0
    for i in range(0, len(padded)-1):
        s1 = padded[i][0] * padded[i+1][1]
        s2 = padded[i][1] * padded[i+1][0]

        area += (s1 - s2) / 2

    return abs(int(area))

def digArea(path: list):
    # Do get the dig area we need to run shoelace, but then also account
    # for the trench itself.
    return shoelace(path) + int(trench_length/2) + 1

area = digArea(trench)
print(f'Area: {area}')