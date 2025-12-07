import re
import sys
from pprint import pprint
from copy import deepcopy
import numpy as np

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
        pprint("".join(row))

# Find start/goal pos
gridW = len(grid[0])
gridH = len(grid)
start = None
goal = None
for x in range(0, gridW):
    if grid[0][x] == '.':
        start = (x, 0)
        break
for x in range(0, gridW):
    if grid[gridH-1][x] == '.':
        goal = (x, gridH-1)
        break
if start is None or goal is None:
    raise Exception('Failed to find start/goal')

printGrid(grid)
print(f'Start: {start}')
print(f'Goal: {goal}')

def buildGraph(grid):
    graph = {}
    
    for y in range(0, gridH):
        for x in range(0, gridW):
            if grid[y][x] == '#':
                continue

            next = []
            dirs = ['R', 'L', 'D', 'U']

            for dir in dirs:
                newX = x
                newY = y

                if   dir == 'R': newX += 1
                elif dir == 'L': newX -= 1
                elif dir == 'D': newY += 1
                elif dir == 'U': newY -= 1

                # out of bounds
                if newX < 0 or newX >= gridW or newY < 0 or newY >= gridH:
                    continue

                val = grid[newY][newX]

                if val == '#':
                    continue

                # if   dir == 'R' and val == '<': continue
                # elif dir == 'L' and val == '>': continue
                # elif dir == 'D' and val == '^': continue
                # elif dir == 'U' and val == 'v': continue

                next.append((newX, newY))

            graph[(x, y)] = next

    return graph

# def buildRecursive(graph):
#     pass

# def isJunction(grid, pos):
#     (x, y) = pos
#     val = grid[y][x]

#     if val == '#':
#         return False
    
#     dir_count = 0
#     dirs = ['R', 'D', 'L', 'U']

#     for dir in dirs:
#         newX = x
#         newY = y

#         if   dir == 'R': newX += 1
#         elif dir == 'L': newX -= 1
#         elif dir == 'U': newY -= 1
#         elif dir == 'D': newY += 1

#         if newX < 0 or newX >= gridW or newY < 0 or newY >= gridH:
#             continue

#         if grid[y][x] == '#':
#             continue

#         dir_count += 1

#     return dir_count > 2

def findJunctions(graph, junction_start):
    junctions = []
    visited = {
        junction_start: True
    }

    # Initialize queue with neighbors from start point
    queue = [(n, 1) for n in graph[junction_start]]

    while len(queue) > 0:
        (cur, dis) = queue.pop(0)
        if cur in visited:
            continue
        visited[cur] = True

        neighbors = graph[cur]
        if len(neighbors) == 2:
            
            queue += [(n, dis+1) for n in neighbors]
        else:
            junctions.append((cur, dis))

    return junctions

def buildJunctionGraph(graph, start):
    junction_graph = {}

    queue = [start]
    while len(queue) > 0:
        cur = queue.pop(0)
        if cur in junction_graph:
            print(f'Junctions already found: {cur}')
            continue

        print(f'Finding junctions for {cur}')
        junctions = findJunctions(graph, cur)
        print(f'Junctions: {junctions}')

        junction_graph[cur] = junctions
        queue += [j[0] for j in junctions]

    return junction_graph
                
graph = buildGraph(grid)
junction_graph = buildJunctionGraph(graph, start)

print(f'Junction graph')
for key in junction_graph:
    print(f'{key}: {junction_graph[key]}')


def findLongestPathRecursive(graph, path, visited, distance, longest):
    global goal
    
    cur = path[len(path)-1]
    neighbors = graph[cur]

    if cur == goal:
        return max(distance, longest)

    for (neighbor, dis) in neighbors:
        if neighbor in visited:
            continue

        path.append(neighbor)
        visited[neighbor] = True

        longest = findLongestPathRecursive(graph, path, visited, distance+dis, longest)

        path.pop()
        del visited[neighbor]

    return longest
    
def findLongestPath(graph, start):
    return findLongestPathRecursive(graph, [start], { start: True }, 0, 0)

longest = findLongestPath(junction_graph, start)
print(f'Longest path: {longest}')