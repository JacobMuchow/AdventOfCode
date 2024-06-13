import re
import sys
sys.setrecursionlimit(1000000)

inputFile = open('input.txt', 'r')
lines = []

# Read lines
while True:
    line = inputFile.readline()
    if not line:
        break

    match = re.match(r'([A-Z]) ([0-9]+) \((.*)\)', line)

    lines.append((match[1], int(match[2]), match[3]))

inputFile.close()

# Build grid
posX = 0
posY = 0
gridWidth = 1
gridHeight = 1

# First we'll figure out the dimensions of the grid.
for line in lines:
    (dir, count, color) = line
    print(f'{dir} {count} {color}')

    if   dir == 'R': posX += count
    elif dir == 'L': posX -= count
    elif dir == 'U': posY -= count
    elif dir == 'D': posY += count

    gridWidth = max(gridWidth, posX+1)
    gridHeight = max(gridHeight, posY+1)

print (f'Grid size: {gridWidth} x {gridHeight}')

# Now, generate a blank grid
grid = []
for y in range(0, gridHeight):
    row = []
    for x in range(0, gridWidth):
        row.append('.')
    grid.append(row)

# Now, traverse the lines again this time marking dig sections.


def printGrid(grid):
    for row in grid:
        print("".join(map(lambda x: str(x), row)))

print('Empty grid:')
printGrid(grid)
print(f'Grid lens: {len(grid[0])} x {len(grid)}')

for line in lines:
    (dir, count, color) = line
    # print(f'{dir} {count} {color}')

    for i in range(1, count+1):
        if   dir == 'R': posX += 1
        elif dir == 'L': posX -= 1
        elif dir == 'D': posY += 1
        elif dir == 'U': posY -= 1
        
        print(f'Mark {posX},{posY}')
        grid[posY][posX] = '#'

print('Grid:')
printGrid(grid)

def posKey(x, y):
    return f'{x},{y}'

def digOrLeave(start):
    global grid

    visited = {}
    path_found = False
    path = [start]

    while len(path) > 0:
        cur = path[len(path)-1]
        curKey = posKey(cur[0], cur[1])
        visited[curKey] = cur

        dirs = ['R', 'D', 'L', 'U']

        go_back = True

        for dir in dirs:
            x = cur[0]
            y = cur[1]

            if   dir == 'R': x += 1
            elif dir == 'L': x -= 1
            elif dir == 'U': y -= 1
            elif dir == 'D': y += 1

            if x < 0 or x >= len(grid[0]) or y < 0 or y >= len(grid):
                path_found = True
                break
            
            next = grid[y][x]
            if next == '#':
                continue

            if next == '_':
                path_found = True
                break

            if x == 0 or x == gridWidth-1 or y == 0 or y == gridHeight-1:
                path_found = True
                break

            if posKey(x, y) in visited:
                continue

            # Bound reached!


            path.append((x, y))
            go_back = False

        if path_found:
            break

        if go_back:
            path.pop()

    if path_found:
        for (x, y) in path:
            grid[y][x] = '_'
    else:
        for key in visited:
            (x, y) = visited[key]
            grid[y][x] = '#'

# Check all nodes to decide if they should be dug out or not
for y in range(0, gridHeight):
    for x in range(0, gridWidth):
        if grid[y][x] != '.':
            continue

        digOrLeave((x, y))

print('New grid:')
printGrid(grid)

total = 0
for y in range(0, gridHeight):
    for x in range(0, gridWidth):
        if grid[y][x] == '#':
            total += 1

print(f'Total filled: {total}')