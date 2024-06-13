import re
import sys
sys.setrecursionlimit(1000000)

inputFile = open('test.txt', 'r')
grid = []

# Read lines
while True:
    line = inputFile.readline()
    if not line:
        break

    row = re.findall(r'.', line)
    row = list(map(lambda x: int(x), row))
    grid.append(row)

inputFile.close()

def printGrid(grid):
    for row in grid:
        print("".join(map(lambda x: str(x), row)))

print('Grid:')
printGrid(grid)

start = (0, 0)
goal = (len(grid[0])-1, len(grid)-1)
print(f'Goal: {goal}, {grid[goal[1]][goal[0]]}')

path = [start]

visited_nodes = {}
best_path = (-1, [])
steps = 0

def posKey(x, y):
    return f'{x},{y}'

def greedyDistancePath():
    global grid
    x = 1
    y = 0
    dir = 'R'
    total_loss = 0
    path = [(0, 0)]

    while True:
        path += [(x, y)]
        total_loss += grid[y][x]

        if x == goal[0] and y == goal[1]:
            break

        if dir == 'R':
            y += 1
            dir = 'D'
        else:
            x += 1
            dir = 'R'

    return (total_loss, path)

def explorePath(path: list, dir: str, dirCount: int, totalLoss: int):
    global grid
    global visited_nodes
    global best_path
    global steps
    (x, y) = path[len(path)-1]
    steps += 1

    if best_path[0] == -1:
        print("Best -1???")

    # print(f'Explore ({x},{y} "{dir}")', 'dir count', dirCount, 'total', totalLoss)
    # print(str(path))

    # out of bounds
    if x < 0 or x >= len(grid[0]) or y < 0 or y >= len(grid):
        # print("Out of Bounds")
        return
    
    # too many times in one dir
    if dirCount >= 3:
        # print("Dir count >= 3")
        return
    
    newTotalLoss = totalLoss + grid[y][x]

    # Total loss will be worse than best case
    best_possible = newTotalLoss + (goal[0] - x) + (goal[1] - y) + grid[goal[1]][goal[0]] - 1
    if best_path[0] != -1 and best_possible >= best_path[0]:
        return

    # goal reached, is this the new best?
    if x == goal[0] and y == goal[1]:
        # print('Goal reached.')
        if best_path[0] == -1 or newTotalLoss < best_path[0]:
            # print('New best path found')
            best_path = (newTotalLoss, path)
        return

    # Skip visited nodes if they were visited with existing total loss.
    # NOTE: this might create a bug if in 1 encouter you came from 'L' and another you came from 'R' because they each allow a allowable dir that the other does not.
    key = f'{x},{y},{dir},{dirCount}'
    if key in visited_nodes:
        # visited = visited_nodes[key]
        # if dirCount
        # visited_nodes[key][0] < totalLoss:;
        # print(f'Point visited. {key} {visited_nodes[key]}')
        # print(f'')
        return
    visited_nodes[key] = (totalLoss, dirCount)#, path.copy())

    # if dir == 'R':
    #     dirs = ['D', 'R', 'L', 'U']
    # else:
    #     dirs = ['R', 'D', 'L', 'U']

    dirs = ['R', 'D', 'L', 'U']

    # Can't go backward
    if   dir == 'R': dirs.remove('L')
    elif dir == 'D': dirs.remove('U')
    elif dir == 'L': dirs.remove('R')
    elif dir == 'U': dirs.remove('D')

    # Greedy traversal
    trav_order = []
    for newDir in dirs:
        if   newDir == 'R': next = (x+1, y)
        elif newDir == 'D': next = (x, y+1)
        elif newDir == 'L': next = (x-1, y)
        elif newDir == 'U': next = (x, y-1)

        trav_order.append((0, next, newDir))

        # Out of bounds
        # if next[0] < 0 or next[0] >= len(grid[0]) or next[1] < 0 or next[1] >= len(grid):
        #     continue

        # next_loss = grid[next[1]][next[0]]
        # inserted = False
        # for i in range(0, len(trav_order)):
        #     if next_loss < trav_order[i][0]:
        #         trav_order.insert(i, (next_loss, next, newDir))
        #         inserted = True
        #         break

        # if not inserted:
        #     trav_order.append((next_loss, next, newDir))

    # print(str(trav_order))

    for (_, next, newDir) in trav_order:
        if   newDir == 'R': explorePath(path + [next], 'R', dirCount+1 if dir == 'R' else 0, newTotalLoss)
        elif newDir == 'D': explorePath(path + [next], 'D', dirCount+1 if dir == 'D' else 0, newTotalLoss)
        elif newDir == 'L': explorePath(path + [next], 'L', dirCount+1 if dir == 'L' else 0, newTotalLoss)
        elif newDir == 'U': explorePath(path + [next], 'U', dirCount+1 if dir == 'U' else 0, newTotalLoss)

        # TODO: also handle dircount <= ~3

# best_path = greedyDistancePath()
# print('Greedy path: ' + str(best_path))

explorePath(path, None, 0, -1 * grid[0][0])

print('\n\nBest path after exploring!')
print(str, best_path)
print(f'Steps used: {steps}')
        
