import re
import sys
from pprint import pprint
sys.setrecursionlimit(1000000)

inputFile = open('input.txt', 'r')
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

def posKey(x, y, axis = None):
    if axis is not None:
        return f'{x},{y},{axis}'
    else:
        return f'{x},{y}'
    
def axisForDir(dir):
    return 'V' if dir == 'U' or dir == 'D' else 'H'

def createGraph(grid):
    graph = {}

    for y in range(0, len(grid)):
        for x in range(0, len(grid[0])):
            for axis in ['V', 'H']:
                neighbors = {}

                dirs = ['R', 'L'] if axis == 'V' else ['D', 'U']
                for dir in dirs:
                    energy = 0
                    for count in range(1, 11):
                        if   dir == 'R': newX = x + count; newY = y
                        elif dir == 'D': newX = x; newY = y + count
                        elif dir == 'L': newX = x - count; newY = y
                        elif dir == 'U': newX = x; newY = y - count

                        if newX < 0 or newX >= len(grid[0]) or newY < 0 or newY >= len(grid):
                            break

                        energy += grid[newY][newX]
                        if count >= 4:
                            neighbors[posKey(newX, newY, axisForDir(dir))] = energy
                        
                graph[posKey(x, y, axis)] = neighbors

    return graph

start = (0, 0)
goal = (len(grid[0])-1, len(grid)-1)

startKeyH = posKey(0, 0, 'H')
startKeyV = posKey(0, 0, 'V')
goalKeyH = posKey(goal[0], goal[1], 'H')
goalKeyV = posKey(goal[0], goal[1], 'V')

graph = createGraph(grid)
print('Graph:')

# Init data for Djikstra algo
distances = {}
previous = {}
visited = {}
queue = []
for y in range(0, len(grid)):
    for x in range(0, len(grid[0])):
        for axis in ['V', 'H']:
            key = posKey(x, y, axis)
            distances[key] = float('inf')
            previous[key] = None
            queue.append(key)
        
distances[startKeyH] = 0
distances[startKeyV] = 0

def nextInQueue(queue, distances):
    dis = float('inf')
    idx = -1

    for i in range(0, len(queue)):
        u = queue[i]
        if distances[u] < dis:
            dis = distances[u]
            idx = i

    return idx

prevDir = None

print('DJIKSTRA')
while len(queue) > 0:
    if len(queue) % 1000 == 0:
        print(f'Queue: {len(queue)}')
    u_key = queue.pop(nextInQueue(queue, distances))
    neighbors = graph[u_key]

    for v_key in neighbors:
        if v_key in visited:
            continue

        v_energy = neighbors[v_key]

        newDistance = distances[u_key] + v_energy
        if newDistance <= distances[v_key]:
            distances[v_key] = newDistance
            previous[v_key] = u_key

print('Energy drain H: ' + str(distances[goalKeyH]))
print('Energy drain V: ' + str(distances[goalKeyV]))

lowest_energy = min(distances[goalKeyH], distances[goalKeyV])
print(f'Lowest energy: {lowest_energy}')

# Create path by tracing backward from goal
path = []
cur = goalKeyV

while True:
    path.insert(0, cur)
    cur = previous[cur]

    if cur == startKeyV or cur == startKeyH:
        break

print('Shorted path')
pprint(path)