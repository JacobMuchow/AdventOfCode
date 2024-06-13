import re
import sys
from pprint import pprint
from copy import deepcopy
import math

sys.setrecursionlimit(1000000)

inputFile = open('input.txt', 'r')

grid = []

# Parse workflows
while True:
    line = inputFile.readline()
    if not line:
        break

    row = re.findall(r'.', line)
    grid.append(row)

inputFile.close()

def printGrid(grid):
    for row in grid:
        print("".join(row))

def posKey(x, y):
    return f'{x},{y}'

printGrid(grid)
gridW = len(grid[0])
gridH = len(grid)

def createGraph(grid):
    graph = {}
    dirs = ['R', 'D', 'L', 'U']

    for y in range(0, gridH):
        for x in range(0, gridW):
            if grid[y][x] == '#':
                continue

            neighbors = {}
            for dir in dirs:
                newX = x
                newY = y

                if dir == 'R': newX += 1
                if dir == 'L': newX -= 1
                if dir == 'D': newY += 1
                if dir == 'U': newY -= 1

                if newX < 0 or newX >= gridW or newY < 0 or newY >= gridH:
                    continue

                if grid[newY][newX] == '#':
                    continue

                neighbors[posKey(newX, newY)] = (newX, newY)

            graph[posKey(x, y)] = neighbors

    return graph

def computeShortestPaths(graph: dict, start: tuple):
    # Djikstra's algorithm
    distances = {}
    previous = {}
    visited = {}
    queue = []

    start_key = posKey(start[0], start[1])

    # Initialize values
    # for y in range(0, len(grid)):
    #     for x in range(0, len(grid[0])):
    #         if grid[y][x] == 
    #         key = posKey(x, y)
    #         distances[key] = float('inf')
    #         previous[key] = None
    #         queue.append(key)

    for key in graph:
        distances[key] = float('inf')
        previous[key] = None
        queue.append(key)
            
    distances[start_key] = 0

    def nextInQueue(queue, distances):
        dis = float('inf')
        idx = -1

        for i in range(0, len(queue)):
            u = queue[i]
            if distances[u] < dis:
                dis = distances[u]
                idx = i

        return idx

    while len(queue) > 0:
        if len(queue) % 1000 == 0:
            print(f'Queue: {len(queue)}')
        
        u_key = queue.pop(nextInQueue(queue, distances))
        neighbors = graph[u_key]

        for n_key in neighbors:
            if n_key in visited:
                continue

            newDistance = distances[u_key] + 1
            if newDistance <= distances[n_key]:
                distances[n_key] = newDistance
                previous[n_key] = u_key

    return distances

graph = createGraph(grid)
# pprint(graph)

distances = computeShortestPaths(graph, (5, 5))

# print('SHORTEST PATHS')
# for key in distances:
#     print(f'{key}: {distances[key]}')

evens = [key for key in distances if distances[key] % 2 == 0]
odds = [key for key in distances if distances[key] % 2 == 1]
evens_val = len(list(map(lambda key: distances[key], evens)))
odds_val = len(list(map(lambda key: distances[key], odds)))

print(f'Full evens: {evens_val}')
print(f'Full odds: {odds_val}')

steps_to_edge = math.floor(gridW / 2)
print(f'Steps to edge: {steps_to_edge}')

evens_corner = [key for key in evens if distances[key] > steps_to_edge]
odds_corner = [key for key in odds if distances[key] > steps_to_edge]
evens_corner_val = len(list(map(lambda key: distances[key], evens_corner)))
odds_corner_val = len(list(map(lambda key: distances[key], odds_corner)))

print(f'Corner evens: {evens_corner_val}')
print(f'Corner odds: {odds_corner_val}')

step_goal = 26501365
n = (step_goal - steps_to_edge) / gridW
print(f'n: {n}') 


total = pow(n, 2) * evens_val + \
        pow(n+1, 2) * odds_val + \
        n * evens_corner_val - \
        (n+1) * odds_corner_val

print(f'Total: {total}')