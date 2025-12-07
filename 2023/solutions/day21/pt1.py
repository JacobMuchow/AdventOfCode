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

def posKey(x, y):
    return f'{x},{y}'

def printGrid(grid):
    for row in grid:
        print("".join(row))

printGrid(grid)

opts = {}
for y in range(0, len(grid)):
    for x in range(0, len(grid[0])):
        if grid[y][x] == 'S':
            opts[posKey(x, y)] = (x, y)

for step in range(0, 10):
    new_opts = {}

    for opt in opts.values():
        for dir in ['R', 'L', 'D', 'U']:
            (x, y) = opt

            if   dir == 'R': x += 1
            elif dir == 'L': x -= 1
            elif dir == 'D': y += 1
            elif dir == 'U': y -= 1

            if x < 0 or x >= len(grid[0]) or y < 0 or y >= len(grid):
                continue

            if grid[y][x] == '#':
                continue

            new_opts[posKey(x, y)] = (x, y)

    opts = new_opts

total_opts = len(opts.values())
print(f'Total opts: {total_opts}')