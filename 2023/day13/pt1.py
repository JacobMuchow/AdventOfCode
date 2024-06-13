import re
import sys

# sys.setrecursionlimit(1_000_000)

inputFile = open('input.txt', 'r')
grids = []
new_grid = []

# Read lines
while True:
    line = inputFile.readline()
    if not line:
        if len(new_grid) > 0:
            grids.append(new_grid)
        break

    line = line.strip()
    
    if line == "":
        grids.append(new_grid)
        new_grid = []
    else:
        new_grid.append(line)

inputFile.close()

def printGrid(grid):
    for line in grid:
        print(line)
    print("")

# Print grids
for i in range(0, len(grids)):
    print(f'Grid {i}')
    printGrid(grids[i])

def mirrors(grid, center, axis="row"):
    if axis == "row":
        # Invalid center
        if center <= 0 or center >= len(grid):
            return False
        
        # Start at center, move out to far edge.
        depth = 0
        while True:
            i = center + depth
            m_i = center - 1 - depth

            # Edge found, mirror complete.
            if i >= len(grid):
                return True
            if m_i < 0:
                return True
            
            if grid[i] != grid[m_i]:
                return False
            
            depth += 1

def findMirrorRow(grid):
    for i in range(1, len(grid)):
        if mirrors(grid, i):
            return i
    return -1

def rotateGrid(grid):
    new_grid = []

    for x in range(0, len(grid[0])):
        chars = []
        for y in range(0, len(grid)):
            chars.insert(0, grid[y][x])
        new_line = "".join(chars)
        new_grid.append(new_line)

    return new_grid

totals = 0

for grid in grids:
    mirror_row = findMirrorRow(grid)
    if mirror_row >= 0:
        totals += 100 * mirror_row
    else:
        rotated = rotateGrid(grid)
        mirror_col = findMirrorRow(rotated)

        if mirror_col >= 0:
            totals += mirror_col
        else:
            print('ERROR could not find row or col!!')

print('Totals: ' + str(totals))