import re
import sys

# sys.setrecursionlimit(1_000_000)

inputFile = open('../../resources/day10/input.txt', 'r')
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

# Find start point in grid
def findStart(grid):
    for y in range(0, len(grid)):
        for x in range(0, len(row)):
            if grid[y][x] == 'S':
                return (x, y)
    raise 'Start not found'

start = findStart(grid)
print('Start: ' + str(start))

class Node:
    def __init__(self, x, y, dir):
        self.x = x
        self.y = y
        self.dir = dir
        self.edge = None
        self.nodes = {}
        self.isLoop = False
        self.type = None
        self.visited = False

    def __str__(self):
        return f'{grid[self.y][self.x]} ({self.x},{self.y}) {self.dir}'

possible_dirs = {
    'S': ['T', 'R', 'B', 'L'],
    '-': ['R', 'L'],
    '|': ['T', 'B'],
    '7': ['L', 'B'],
    'J': ['T', 'L'],
    'L': ['R', 'T'],
    'F': ['B', 'R'],
}

def make_node(cur: Node, dir: str):

    # 1) Ignore the direction you just came from
    if dir == 'T' and cur.dir == 'B':
        return None
    if dir == 'B' and cur.dir == 'T':
        return None
    if dir == 'R' and cur.dir == 'L':
        return None
    if dir == 'L' and cur.dir == 'R':
        return None

    # 2) Ensure the bounds are valid
    x = cur.x
    y = cur.y

    if dir == 'R': x += 1
    elif dir == 'L': x -= 1
    elif dir == 'T': y -= 1
    elif dir == 'B': y += 1
    else: raise f'Error: invalid dir {dir}'

    if x < 0 or x >= len(grid[0]) or y < 0 or y >= len(grid):
        return None
    
    # 3) Ensure the new node has a proper receptor
    type = grid[y][x]

    if type == 'S':
        return Node(x, y, dir)
    if type == '.':
        return None
    
    bound_check = None

    if type == '-':
        if dir == 'R': bound_check = 'R'
        elif dir == 'L': bound_check = 'L'
        else: return None
    
    if type == '|':
        if dir == 'T': bound_check = 'T'
        elif dir == 'B': bound_check = 'B'
        else: return None
    
    if type == '7':
        # print(f'7 Dir: {self.dir}')
        if dir == 'R': bound_check = 'B'
        elif dir == 'T': bound_check = 'L'
        else: return None

    if type == 'J':
        if dir == 'B': bound_check = 'L'
        elif dir == 'R': bound_check = 'T'
        else: return None

    if type == 'L':
        if dir == 'L': bound_check = 'T'
        elif dir == 'B': bound_check = 'R'
        else: return None

    if type == 'F':
        if dir == 'T': bound_check = 'R'
        elif dir == 'L': bound_check = 'B'
        else: return None

    # print(f'Bound check: {bound_check}')
        
    # if bound_check == 'R' and x+1 < len(grid[0]):
    #     return None
    # if bound_check == 'L':
    #     return True if self.x > 0 else False
    # if bound_check == 'B':
    #     # print(f'y: {self.y}, len: {len(grid)}')
    #     return True if self.y < len(grid)-1 else False
    # if bound_check == 'T':
    #     return True if self.y > 0 else False
    
    # raise 'Impossible situation'
    
    return Node(x, y, dir)

def dfs_iter(start: Node):
    path = [start]

    while len(path) > 0:
        cur_node = path[len(path)-1]
        cur_type = grid[cur_node.y][cur_node.x]
        print(f'\n\nLoop: {cur_node}')

        if cur_type == 'S' and len(path) > 1:
            return path
        
        unwind = True
        
        dirs = possible_dirs[cur_type]
        for dir in dirs:
            if dir in cur_node.nodes:
                continue

            new_node = make_node(cur_node, dir)
            cur_node.nodes[dir] = new_node

            if new_node:
                path.append(new_node)
                unwind = False
                break
        
        if unwind:
            path.pop()

    return None


start_node = Node(start[0], start[1], None)
path = dfs_iter(start_node)


# path = [start_node]
# path = dfs(start_node, path)

print('Solution found!')
for node in path:
    print(str(node))

distance = int((len(path) - 1) / 2)
print(f'Path length: {distance}')

node_grid = []

for y in range(0, len(grid)):
    node_row = []

    for x in range(0, len(grid[0])):
        node = Node(x, y, None)
        node.type = '.'
        node.isLoop = False
        node_row.append(node)

    node_grid.append(node_row)

for loop_node in path:
    node = node_grid[loop_node.y][loop_node.x]
    node.type = grid[loop_node.y][loop_node.x]
    node.isLoop = True


def print_node_grid(grid):
    for row in grid:
        str = ''
        for node in row:
            str += node.type
        print(str)

def path_to_exit(grid, start_node):
    print('path_to_exit ' + str(start_node))
    path = [start_node]

    while len(path) > 0:
        node = path[len(path)-1]
        node.visited = True

        dirs = ['T', 'R', 'B', 'L']

        print(f'{node.type} Dir: {node.dir}, Edge: {node.edge}')
        
        if node.type == '-':
            if node.dir == 'T' or node.dir == 'B':
                node.edge = 'B' if node.dir == 'T' else 'T'
                dirs = ['R', 'L']
            else:
                dirs = ['R', 'L']
                dirs.append(node.edge)

        elif node.type == '|':
            if node.dir == 'R' or node.dir == 'L':
                node.edge = node.dir
                dirs = ['T', 'B']
            else:
                dirs = ['T', 'B']
                dirs.append(node.edge)

        elif node.type == '7':
            if node.dir == 'R':
                if node.edge == 'B':
                    dirs = ['B']
                    node.edge = 'L'
                if node.edge == 'T':
                    dirs = ['T', 'R', 'B']
            # TODO: others...
            if node.dir == 'B':
                if node.edge == 'R':
                    dirs = ['T', 'R', 'L']
                    node.edge = 'T'
                    
        elif node.type == 'J':
            if node.dir == 'B':
                if node.edge == 'L':
                    dirs = ['L']
                    node.edge = 'T'
            if node.dir == 'R':
                if node.edge == 'B':
                    dirs = ['T', 'R', 'B']
                    node.edge = 'R' # Doesn't edge depend on dir? possibly: set next node edge depending on edge + type of prev
                    
                
        elif node.type == 'L':
            if node.dir == 'L':
                if node.edge == 'T':
                    dirs = ['T']
                    node.edge = 'R'
            if node.dir == 'T':
                if node.edge == 'L':
                    dirs = ['R', 'B', 'L']
                    node.edge = 'B'
        
        elif node.type == 'F':
            if node.dir == 'T':
                if node.edge == 'R':
                    dirs = ['R']
                    node.edge = 'B'
            if node.dir == 'L':
                if node.edge == 'T':
                    dirs = ['T', 'B', 'L']
                    node.edge = 'L'
            
        # elif node.type == '|':
        #     if node.dir == 'B' or node.dir 
            
        elif node.type == 'F' or node.type == 'L':
            if node.dir == 'B' or node.dir == 'T':
                dirs = ['T', 'R', 'B', 'L']
            else:
                dirs = None

        elif node.type == '7' or node.type == 'J' or node.type == 'L' or node.type == 'F':
            dirs = None

        if dirs is None:
            print('back')
            node.dir = None # issue?
            node.edge = None
            path.pop()
            continue
        
        unwind = True
        
        for dir in dirs:
            if dir in node.nodes:
                continue

            x = node.x
            y = node.y

            if dir == 'R': x += 1
            elif dir == 'L': x -= 1
            elif dir == 'T': y -= 1
            elif dir == 'B': y += 1
            else: raise f'Error: invalid dir {dir}'

            try:
                next = grid[y][x]
                print(str(next))
            except Exception as e:
                print(f'Error at {x},{y}')
                raise e

            if next.type == 'O':
                return path
            
            if next.visited:
                continue

            next.dir = dir
            if node.edge:
                next.edge = node.edge

            node.nodes[dir] = next
            path.append(next)
            unwind = False
            break

        if unwind:
            node.edge = None
            path.pop()

    return None


# Fill out outer edge
for y in range(0, len(grid)):
    for x in range(0, len(grid[0])):
        node = node_grid[y][x]

        # Already solved
        if node.isLoop or node.type == 'O' or node.type == 'I':
            continue

        if node.type == '.':
            # Anything touching outer edge is Out.
            if y == 0 or y == len(grid)-1 or x == 0 or x == len(grid[0])-1:
                node_grid[y][x].type = 'O'
                continue

# # Test all points for In/Out
# for y in range(0, len(grid)):
#     for x in range(0, len(grid[0])):
#         node = node_grid[y][x]

#         # Already solved
#         if node.isLoop or node.type == 'O' or node.type == 'I':
#             continue

#         if node.type == '.':
#             path = path_to_exit(node_grid, node)

#             if not path:
#                 print('No path found!')
#             else:
#                 for node in path:
#                     if node.type == '.':
#                         node.type = 'O'

# # All remaining area is "inside" the loop.
# area = 0
# for row in node_grid:
#     for node in row:
#         if node.type == '.':
#             node.type = 'I'
#             area += 1

test_node = node_grid[6][2]
path = path_to_exit(node_grid, test_node)

if not path:
    print('No path found!')
else:
    print('Path found.')
    for node in path:
        print(str(node))
        # if node.type == '.':
        #     node.type = 'O'

print('Node Grid:')
print_node_grid(node_grid)

# print('Area in loop: ' + str(area))
