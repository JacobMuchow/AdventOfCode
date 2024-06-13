import re
import sys

# sys.setrecursionlimit(1_000_000)

inputFile = open('input.txt', 'r')
grid = []
start = None

# Read lines
while True:
    line = inputFile.readline()
    if not line:
        break
    row = re.findall(r'.', line)
    grid.append(row)
inputFile.close()

galaxies = []
expanded_rows = []
expanded_cols = []

# Find rows that need to be expanded
for y in range(0, len(grid)):
    galaxy_in_row = False

    for x in range(0, len(grid[y])):
        if grid[y][x] == '#':
            galaxy_in_row = True
            break

    if not galaxy_in_row:
        expanded_rows.append(y)

# Find cols that need to be expanded
for x in range(0, len(grid[0])):
    galaxy_in_col = False

    for y in range(0, len(grid)):
        if grid[y][x] == '#':
            galaxy_in_col = True
            break

    if not galaxy_in_col:
        expanded_cols.append(x)

print('Universe:')
for row in grid:
    print(row)

print('Expanded Rows', str(expanded_rows))
print('Expanded Cols', str(expanded_cols))

# Expand universe
dy = 0
for y in expanded_rows:
    new_row = grid[y+dy].copy()
    for x in range(0, len(new_row)):
        new_row[x] = '@'
    grid.insert(y+dy, new_row)
    dy += 1

dx = 0
for x in expanded_cols:
    for row in grid:
        row.insert(x+dx, '@')
    dx += 1

# Build list of galaxy locations
for y in range(0, len(grid)):
    for x in range(0, len(grid[y])):
        if grid[y][x] == '#':
            galaxies.append((x, y))

def shortestPath(g1, g2):
    # dis_x = abs(g2[0] - g1[0])
    # dis_y = abs(g2[1] - g1[1])

    dist = 0
    x1 = min(g1[0], g2[0])
    x2 = max(g1[0], g2[0])
    for x in range(x1, x2):
        if grid[0][x] == '@':
            dist += 1000000 - 1
        else:
            dist += 1
    
    y1 = min(g1[1], g2[1])
    y2 = max(g1[1], g2[1])
    for y in range(y1, y2):
        if grid[y][0] == '@':
            dist += 1000000 - 1
        else:
            dist += 1

    return dist

print('Expanded Universe:')
for row in grid:
    print(row)

total = 0
count = 0

for i in range(0, len(galaxies)):
    g1 = galaxies[i]

    for j in range(i+1, len(galaxies)):
        g2 = galaxies[j]

        path = shortestPath(g1, g2)
        # print(f'Path {i+1}-{j+1}: {path}')
        total += path

        count += 1

print('Count: ' + str(count))
print('Total: ' + str(total))