import re
import sys
from pprint import pprint
from copy import deepcopy
import numpy as np

sys.setrecursionlimit(1000000)

inputFile = open('test.txt', 'r')

stones = []

# Parse stones
while True:
    line = inputFile.readline()
    if not line:
        break

    row = re.findall(r'[0-9\-]+', line)
    row = list(map(lambda x: float(x), row))

    p = [row[0], row[1], row[2]]
    v = [row[3], row[4], row[5]]

    stones.append((p, v))

inputFile.close()

def linearEq(stone):
    (p, v) = stone

    if (v[0] == 0 or v[1] == 0):
        return (None, None)

    m = v[1] / v[0]
    b = p[1] - m * p[0]

    return (m, b)

def intersection(stone1, stone2):
    (m1, b1) = linearEq(stone1)
    (m2, b2) = linearEq(stone2)

    if m1 is None or m2 is None:
        return None

    if m1 == m2:
        return None

    x = (b2 - b1) / (m1 - m2)
    y = m1 * x + b1

    return (x, y)

def isInFuture(stone, intersection):
    startX = stone[0][0]
    velX = stone[1][0]

    if velX > 0:
        return intersection[0] > startX
    else:
        return intersection[0] < startX

def testXYIntersection(stoneA, stoneB):
    point = intersection(stoneA, stoneB)

    if point is None:
        return False
    
    if point[0] % 1.0 != 0 or point[1] % 1.0 != 0:
        return False

    if not isInFuture(stoneA, point) or not isInFuture(stoneB, point):
        return False
    
    return True

def testZIntersection(stoneA, stoneB):
    (x, y) = intersection(stoneA, stoneB)

    (p1, v1) = stoneA
    (p2, v2) = stoneB

    zA = v1[2] * x + p1[2]
    zB = v2[2] * x + p2[2]

    return zA == zB

stoneA = deepcopy(stones[0])
stoneB = deepcopy(stones[1])

print(f'Stone A: {stoneA}')
print(f'Stone B: {stoneB}')

for x_mag in range(0, 1000):
    for y_mag in range(0, 1000):
        signs = [
            [+1, +1, 1],
            [+1, -1, 1],
            [-1, +1, 1],
            [-1, -1, 1]
        ]

        for sign in signs:
            x_delta = x_mag * sign[0]
            y_delta = y_mag * sign[1]

            stoneA[1][0] += x_delta
            stoneB[1][0] += x_delta
            stoneA[1][1] += y_delta
            stoneB[1][1] += y_delta

            test = testXYIntersection(stoneA, stoneB)
            if test:
                test2 = testZIntersection(stoneA, stoneB)
                if test2:
                    print(f'Candidate! {x_delta}, {y_delta}')

            stoneA[1][0] -= x_delta
            stoneB[1][0] -= x_delta
            stoneA[1][1] -= y_delta
            stoneB[1][1] -= y_delta
