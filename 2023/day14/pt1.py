import re

inputFile = open('input.txt', 'r')
grid = []

# Read lines
while True:
    line = inputFile.readline()
    if not line:
        break

    row = re.findall(r'.', line)
    grid.append(row)

inputFile.close()

class Memoize:
    def __init__(self, f):
        self.f = f
        self.memo = {}
    def __call__(self, *args):
        key = str(args)
        if not key in self.memo:
            self.memo[key] = self.f(*args)
        #Warning: You may wish to do a deepcopy here if returning objects
        return self.memo[key]

def memoize(func):
    records = {}

    def wrapped(grid, *args):
        key = gridKey(grid) 
        # TODO: add back args
        
        #+ ("" if args is None else str(args))
        # print('Key: ' + key)
        #if args is not None:
            #key += str(*args)
        
        if key in records:
            print('Record found: ' + key)
            return (key, records[key])
        
        result = func(grid, *args)
        records[key] = result
        return (key, result)
    
    return wrapped

def printGrid(grid):
    for row in grid:
        print("".join(row))
    print("")

def gridKey(grid):
    str = ''
    o_count = 0
    for y in range(0, len(grid)):
        for x in range(0, len(grid[y])):
            str += grid[y][x]
            if grid[y][x] == 'O':
                o_count += 1
    # print(f'O count {str} {o_count}')
    return str

def moveRockUp(grid, rockX, rockY):
    if grid[rockY][rockX] != "O":
        return
    
    y = rockY - 1
    while y >= 0:
        if grid[y][rockX] != '.':
            break

        y -= 1

    y += 1
    if y != rockY:
        grid[y][rockX] = 'O'
        grid[rockY][rockX] = '.'

moveRockUpMemo = Memoize(moveRockUp)

def tiltColUp(grid, x):
    for y in range(1, len(grid)):
        moveRockUp(grid, x, y)

def moveRockDown(grid, rockX, rockY):
    if grid[rockY][rockX] != "O":
        return
    
    y = rockY + 1
    while y < len(grid):
        if grid[y][rockX] != '.':
            break

        y += 1

    y -= 1
    if y != rockY:
        grid[y][rockX] = 'O'
        grid[rockY][rockX] = '.'

moveRockDownMemo = Memoize(moveRockDown)

def tiltColDown(grid, x):
    for y in range(len(grid)-1, -1, -1):
        moveRockDown(grid, x, y)

def moveRockLeft(grid, rockX, rockY):
    if grid[rockY][rockX] != "O":
        return
    
    x = rockX - 1
    while x >= 0:
        if grid[rockY][x] != '.':
            break
        x -= 1
    x +=1
    if x != rockX:
        grid[rockY][x] = 'O'
        grid[rockY][rockX] = '.'

moveRockLeftMemo = Memoize(moveRockLeft)
    
def tiltRowLeft(grid, y):
    for x in range(1, len(grid[y])):
        moveRockLeft(grid, x, y)

def moveRockRight(grid, rockX, rockY):
    if grid[rockY][rockX] != "O":
        return
    
    x = rockX + 1
    while x < len(grid):
        if grid[rockY][x] != '.':
            break
        x += 1
    x -= 1

    if x != rockX:
        grid[rockY][x] = 'O'
        grid[rockY][rockX] = '.'

moveRockRightMemo = Memoize(moveRockRight)
    
def tiltRowRight(grid, y):
    for x in range(len(grid[y]) - 1, -1, -1):
        moveRockRight(grid, x, y)

tiltColUpMemo = Memoize(tiltColUp)
tiltColDownMemo = Memoize(tiltColDown)
tiltRowLeftMemo = Memoize(tiltRowLeft)
tiltRowRightMemo = Memoize(tiltRowRight)

def tiltGridUp(grid):
    for x in range(0, len(grid[0])):
        tiltColUp(grid, x)

def tiltGridDown(grid):
    for x in range(0, len(grid[0])):
        tiltColDown(grid, x)

def tiltGridLeft(grid):
    for y in range(0, len(grid)):
        tiltRowLeft(grid, y)

def tiltGridRight(grid):
    for y in range(0, len(grid)):
        tiltRowRight(grid, y)

tiltGridUpMemo = Memoize(tiltGridUp)
tiltGridDownMemo = Memoize(tiltGridDown)
tiltGridLeftMemo = Memoize(tiltGridLeft)
tiltGridRightMemo = Memoize(tiltGridRight)

def tiltCycle(grid):
    grid = grid.copy()
    tiltGridUp(grid)
    tiltGridLeft(grid)
    tiltGridDown(grid)
    tiltGridRight(grid)
    return grid

tiltCycleMemo = memoize(tiltCycle)

tilt_cache = {}
grids_seen = {}
keys = []
soln_key = ""
diff = -1

# for i in range(0, 25):
#     key = gridKey(grid)

#     if key in tilt_cache:
#         tilt_cache[key].append(i)
#     else:
#         tilt_cache[key] = [i]

#     tiltCycle(grid)

# print('Tilt cache:')
# for key in tilt_cache:
#     print(f'{key}: {tilt_cache[key]}')

for i in range(0, 1_000_000_000):
                  #  29_900_000
# for i in range(0, 100):
    if i % 10000 == 0:
        print(f'Step {i}')
    # print(f'Grid {i}')
    # printGrid(grid)

    key = gridKey(grid)
    # if not key in tilt_cache:
    #     tiltCycle(grid)
    # # else:
    #     # print('Record hit')
    
    # tilt_cache[key] = grid

    if key in tilt_cache:
        old_i = tilt_cache[key]
        print(f'Key in cache. prev: {old_i}, new: {i}')
        diff = i - old_i
        print(f'Diff: {diff}')

        cycles_left = 1_000_000_000 - i
        remainder = cycles_left % diff
        print(f'Cycles left: {cycles_left}, Remainder: {remainder}')

        # Run X more cycles
        print(f'Running {remainder} more cycles...')
        for j in range(0, remainder):
            tiltCycle(grid)

        break

    tiltCycle(grid)
    tilt_cache[key] = i

# print('Final Grid')
# printGrid(grid)

# for i in range(0, 100000):
#     print(str(i))
#     (key, _) = tiltCycleMemo(grid)
#     print('Key to check: ' + key)

#     if key in grids_seen:
#         grids_seen[key].append(i)
        
#         if len(grids_seen[key]) >= 5:
#             soln_key = key
#             break
#     else:
#        grids_seen[key] = [i]
    
# print(f'Soln key: {soln_key}')
# print(str(grids_seen[soln_key]))

# all_equal = True
# key = keys[0]
# for k in keys:
#     if k != key:
#         all_equal = False

# print(f'All equal: {all_equal}')

total = 0

for y in range(0, len(grid)):
    for x in range(0, len(grid[y])):
        if grid[y][x] == 'O':
            total += len(grid) - y

print('Total Load: ' + str(total))