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

            graph[(x, y)] = {
                "next": next
            }

    return graph

graph = buildGraph(grid)
print(f'GRAPH:')
for key in graph:
    print(f'{key}: {graph[key]["next"]}')


def findLongestPathRecursive(path, visited, longest):
    global graph, goal
    
    cur = path[len(path)-1]
    neighbors = graph[cur]["next"]

    if cur == goal:
        if len(path) > len(longest):
            return path.copy()
        else:
            return longest

    for neighbor in neighbors:
        if neighbor in visited:
            continue

        path.append(neighbor)
        visited[neighbor] = True

        longest = findLongestPathRecursive(path, visited, longest)

        path.pop()
        del visited[neighbor]

    return longest
    
def findLongestPath():
    global graph, start
    return findLongestPathRecursive([start], { start: True }, [])


longest = findLongestPath()
steps = len(longest)-1
print(f'Longest steps: {steps}')