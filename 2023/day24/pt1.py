import re
import sys
from pprint import pprint
from copy import deepcopy
import numpy as np

sys.setrecursionlimit(1000000)

inputFile = open('input.txt', 'r')

stones = []

# Parse stones
while True:
    line = inputFile.readline()
    if not line:
        break

    row = re.findall(r'[0-9\-]+', line)
    row = list(map(lambda x: float(x), row))

    p = (row[0], row[1], row[2])
    v = (row[3], row[4], row[5])

    stones.append((p, v))

inputFile.close()

for stone in stones:
    print(str(stone))

stoneA = stones[0]
stoneB = stones[1]

linear_memo = {}

def linearEq(stone):
    if stone in linear_memo:
        return linear_memo[stone]
    
    (p, v) = stone

    m = v[1] / v[0]
    b = p[1] - m * p[0]

    linear_memo[stone] = (m, b)
    return (m, b)

def intersection(stone1, stone2):
    (m1, b1) = linearEq(stone1)
    (m2, b2) = linearEq(stone2)

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

def countIntersections(stones, boundMin, boundMax):
    count = 0

    for a in range(0, len(stones)-1):
        for b in range(a+1, len(stones)):
            point = intersection(stones[a], stones[b])

            if point is None:
                print(f'Stones {a} and {b} do not intersect')
                continue

            if not isInFuture(stones[a], point):
                print(f'Stones {a} and {b} intersect in stone {a}\'s past')
                continue

            if not isInFuture(stones[b], point):
                print(f'Stones {a} and {b} intersect in stone {b}\'s past')
                continue

            if point[0] < boundMin or point[0] > boundMax or point[1] < boundMin or point[1] > boundMax:
                print(f'Stones {a} and {b} intersect outside bounds')
                continue

            count += 1

    return count

count = countIntersections(stones, 200000000000000, 400000000000000)
print(f'Num intersections: {count}')
