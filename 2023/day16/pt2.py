import re
import sys
sys.setrecursionlimit(1000000)

inputFile = open('input.txt', 'r')
grid = []

# Read lines
while True:
    line = inputFile.readline()
    if not line:
        break

    row = re.findall(r'.', line)
    grid.append(row)

inputFile.close()

energy_grid = []
for y in range(0, len(grid)):
    energy_grid.append([])
    for x in range(0, len(grid[y])):
        energy_grid[y].append('.')

projection_memo = {}

def printGrid(grid):
    for row in grid:
        print("".join(row))

def projectBeam(grid, x, y, dir):
    # print('project', str(x), str(y), dir)
    # Out of bounds
    if x < 0 or x >= len(grid[0]) or y < 0 or y >= len(grid):
        return
    
    memo_key = f'{x},{y},{dir}'
    if memo_key in projection_memo:
        return
    projection_memo[memo_key] = True
    energy_grid[y][x] = '#'
    
    space = grid[y][x]
    
    if space == '.':
        if   dir == 'R': projectBeam(grid, x+1, y,   'R')
        elif dir == 'L': projectBeam(grid, x-1, y,   'L')
        elif dir == 'D': projectBeam(grid, x,   y+1, 'D')
        elif dir == 'U': projectBeam(grid, x,   y-1, 'U')
    elif space == '-':
        if   dir == 'R': projectBeam(grid, x+1, y, 'R')
        elif dir == 'L': projectBeam(grid, x-1, y, 'L')
        elif dir == 'D':
            projectBeam(grid, x+1, y, 'R')
            projectBeam(grid, x-1, y, 'L')
        elif dir == 'U':
            projectBeam(grid, x+1, y, 'R')
            projectBeam(grid, x-1, y, 'L')
    elif space == '|':
        if   dir == 'D': projectBeam(grid, x, y+1, 'D')
        elif dir == 'U': projectBeam(grid, x, y-1, 'U')
        elif dir == 'R':
            projectBeam(grid, x, y+1, 'D')
            projectBeam(grid, x, y-1, 'U')
        elif dir == 'L':
            projectBeam(grid, x, y+1, 'D')
            projectBeam(grid, x, y-1, 'U')
    elif space == '/':
        if   dir == 'R': projectBeam(grid, x, y-1, 'U')
        elif dir == 'L': projectBeam(grid, x, y+1, 'D')
        elif dir == 'D': projectBeam(grid, x-1, y, 'L')
        elif dir == 'U': projectBeam(grid, x+1, y, 'R')
    elif space == '\\':
        if   dir == 'R': projectBeam(grid, x, y+1, 'D')
        elif dir == 'L': projectBeam(grid, x, y-1, 'U')
        elif dir == 'D': projectBeam(grid, x+1, y, 'R')
        elif dir == 'U': projectBeam(grid, x-1, y, 'L')
    else:
        raise f'Unknown space type: "{space}"'

print('Grid:')
printGrid(grid)

def energyForConfig(grid, x, y, dir):
    # Reset projection_memo and enery_grid
    projection_memo.clear()
    for i in range(0, len(energy_grid)):
        for j in range(0, len(energy_grid[y])):
            energy_grid[i][j] = '.'

    projectBeam(grid, x, y, dir)

    energy = 0
    for row in energy_grid:
        for tile in row:
            if tile == '#':
                energy += 1
    
    return energy

# x, y, enery
max = (-1, -1, 0)

for x in range(0, len(grid[0])):
    # All down vectors
    energy = energyForConfig(grid, x, 0, 'D')
    if energy > max[2]:
        max = (x, 0, energy)

    # All up vectors
    energy = energyForConfig(grid, x, len(grid)-1, 'U')
    if energy > max[2]:
        max = (x, len(grid)-1, energy)

for y in range(0, len(grid)):
    # All right vectors
    energy = energyForConfig(grid, 0, y, 'R')
    if energy > max[2]:
        max = (0, y, energy)

    # All left vectors
    energy = energyForConfig(grid, len(grid[0])-1, y, 'L')
    if energy > max[2]:
        max = (len(grid[0])-1, y, energy)

print(f'Max config: {max}')
