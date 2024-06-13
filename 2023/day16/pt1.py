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

projectBeam(grid, 0, 0, 'R')

print('\nEnergy Grid:')
printGrid(energy_grid)

tile_count = 0
for row in energy_grid:
    for tile in row:
        if tile == '#':
            tile_count += 1

print(f'Total Enery: {tile_count}')