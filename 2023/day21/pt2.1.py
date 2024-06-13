import re
import sys
from pprint import pprint
from copy import deepcopy

sys.setrecursionlimit(1000000)

inputFile = open('test.txt', 'r')

grid = []

# Parse workflows
while True:
    line = inputFile.readline()
    if not line:
        break

    row = re.findall(r'.', line)
    grid.append(row)

inputFile.close()

def gridKey(gridX, gridY):
    return f'{gridX}:{gridY}'

def posKey(x, y):
    return f'{x},{y}'

def printGrid(grid):
    for row in grid:
        print("".join(row))

printGrid(grid)
gridW = len(grid[0])
gridH = len(grid)

opts = {}
evens = {}
odds = {}

for y in range(0, gridH):
    for x in range(0, gridW):
        if grid[y][x] == 'S':
            opts[gridKey(0, 0)] = {
                posKey(x, y): (x, y)
            }
            # evens[posKey(0, 0, x, y)] = (0, 0, x, y)

grid_memo = {}

for step in range(1, 5000):
    new_opts = {}

    for grid_key in opts:
        grid_opts = opts[gridKey]

        memo_key = str(grid_opts)
        if memo_key in grid_memo:

        for dir in ['R', 'L', 'D', 'U']:
            (gridX, gridY, x, y) = opt

            if   dir == 'R': x += 1
            elif dir == 'L': x -= 1
            elif dir == 'D': y += 1
            elif dir == 'U': y -= 1

            # if x < 0 or x >= len(grid[0]) or y < 0 or y >= len(grid):
            #     continue

            if x < 0:
                gridX -= 1
                x = gridW - 1
            elif x >= gridW:
                gridX += 1
                x = 0
            
            if y < 0:
                gridY -= 1
                y = gridH - 1
            elif y >= gridH:
                gridY += 1
                y = 0

            if grid[y][x] == '#':
                continue

            key = posKey(gridX, gridY, x, y)

            if odd_step:
                if not key in odds:
                    odds[key] = (gridX, gridY, x, y)
                    new_opts[key] = (gridX, gridY, x, y)
            else:
                if not key in evens:
                    evens[key] = (gridX, gridY, x, y)
                    new_opts[key] = (gridX, gridY, x, y)

    opts = new_opts

    # if odd_step:
    #     print(f'Odds: {odds.keys()}')
    # else:
    #     print(f'Evens: {evens.keys()}')

total_opts = len(evens.values())
print(f'Total opts: {total_opts}')