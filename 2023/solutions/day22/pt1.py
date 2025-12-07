import re
import sys
from pprint import pprint
from copy import deepcopy
import numpy as np

sys.setrecursionlimit(1000000)

inputFile = open('input.txt', 'r')

bricks = []
NO_AXIS = -1
X = 0
Y = 1
Z = 2
gridW = 0
gridH = 0

# Parse workflows
while True:
    line = inputFile.readline()
    if not line:
        break

    tokens = line.split('~')
    p1 = re.findall(r'[0-9]+', tokens[0])
    p2 = re.findall(r'[0-9]+', tokens[1])

    p1 = list(map(lambda x: int(x), p1))
    p2 = list(map(lambda x: int(x), p2))

    axis = NO_AXIS
    for i in range(0, 3):
        if p1[i] != p2[i]:
            if axis != NO_AXIS:
                raise Exception('Bigger bricks??')
            axis = i
    
    new_brick = {
        "p1": p1,
        "p2": p2,
        "axis": axis,
        "len": p2[axis] - p1[axis] + 1,
        "zStart": min(p1[2], p2[2]),
        "up": [],
        "down": []
    }

    gridW = max(gridW, p1[0]+1, p2[0]+1)
    gridH = max(gridH, p1[1]+1, p2[1]+1)

    bricks.append(new_brick)

inputFile.close()

# Sort bricks by starting z pos
bricks = sorted(bricks, key=lambda b: min(b["p1"][2], b["p2"][2]))

# Print bricks
for i in range(0, len(bricks)):
    # print(str(bricks[i]))
    bricks[i]["num"] = i
# print(f'Area: {gridW}x{gridH}')

grid_zMax = np.zeros((gridW, gridH))

for i in range(0, len(bricks)):
    brick = bricks[i]
    # print(f'Testing brick: {brick}')
    num = brick["num"]
    p1 = brick["p1"]
    p2 = brick["p2"]
    axis = brick["axis"]
    zStart = min(p1[2], p2[2])

    mat = np.zeros((gridW, gridH))

    if axis == 2 or axis == NO_AXIS:
        x = p1[0]
        y = p1[1]

        if p2[0] != x: raise Exception('0')
        if p2[1] != y: raise Exception('1')
        z = grid_zMax[y][x]+1 # 3 -> 4

        if zStart < z:
            raise Exception(f"Unexpected case, zStart less than zMax")
        
        delta = zStart - z  # 10 - 4 = 6
        p1[2] -= delta  # 
        p2[2] -= delta
        brick["zStart"] = z
        grid_zMax[y][x] = max(p1[2], p2[2])
        mat[y][x] = 1

    elif axis == 0:
        y = p1[1]
        if p2[1] != y: raise Exception('2')

        x_low = min(p1[0], p2[0])
        x_high = max(p1[0], p2[0])
        z_max = 0

        if x_low == x_high: raise Exception('2.1')

        for x in range(x_low, x_high+1):
            z_max = max(z_max, grid_zMax[y][x])
            mat[y][x] = 1

        z = z_max + 1
            
        if zStart < z:
            raise Exception(f"Unexpected case, zStart less than zMax")
        
        p1[2] = z
        p2[2] = z
        brick["zStart"] = z

        for x in range(x_low, x_high+1):
            grid_zMax[y][x] = z

    elif axis == 1:
        x = p1[0]
        if p2[0] != x: raise Exception('2')

        y_low = min(p1[1], p2[1])
        y_high = max(p1[1], p2[1])
        z_max = 0

        if y_low == y_high: raise Exception('2.1')

        for y in range(y_low, y_high+1):
            z_max = max(z_max, grid_zMax[y][x])
            mat[y][x] = 1

        z = z_max + 1
            
        if zStart < z:
            raise Exception(f"Unexpected case, zStart less than zMax")
        
        p1[2] = z
        p2[2] = z
        brick["zStart"] = z

        for y in range(y_low, y_high+1):
            grid_zMax[y][x] = z

    else:
        raise Exception(f'Invalid axis: {axis}')
    
    brick["mat"] = mat

bricks = sorted(bricks, key=lambda b: min(b["p1"][2], b["p2"][2]))

print("BRICKS AFTER:")
for brick in bricks:
    print(f'{brick["p1"]} - {brick["p2"]}')

for i in range(0, len(bricks)):
    p1 = bricks[i]["p1"]
    p2 = bricks[i]["p2"]
    zi = max(p1[2], p2[2])
    j = i
    # print(f"Testing brick {i}. z: {zi}")

    while True:
        j += 1
        if j >= len(bricks):
            break

        jp1 = bricks[j]["p1"]
        jp2 = bricks[j]["p2"]
        zj = min(jp1[2], jp2[2])

        if zj <= zi:
            continue

        # Over 1 level up... done looping
        if zj > zi+1:
            break

        # 1 level up... evaluate if they cross section
        cross_sum = np.max(np.multiply(bricks[i]["mat"], bricks[j]["mat"]))
        if cross_sum == 0:
            continue
        else:
            # print(f"{i} crosses with {j}")
            bricks[i]["up"].append(j)
            bricks[j]["down"].append(i)

count = 0

for i in range(0, len(bricks)):
    disintegrate = True

    for iu in bricks[i]["up"]:
        if len(bricks[iu]["down"]) <= 1:
            disintegrate = False

    if disintegrate:
        # print(f'Can disintegrate: {i}')
        count += 1

# print("BRICKS AFTER:")
# for brick in bricks:
#     print(f'{brick["p1"]} - {brick["p2"]}')

print(f'Disintegration count: {count}')
print(f'Num bricks: {len(bricks)}')

a = 1
b = 1.0

print(f'ab: {a} {b} equal: {a == b}')