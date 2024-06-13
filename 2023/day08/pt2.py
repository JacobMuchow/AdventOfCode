import re
import numpy

inputFile = open('input.txt', 'r')

turns_raw = inputFile.readline()
turns = re.findall(r'([LR])', turns_raw)

print(f'Turns: {turns}')

# ignore
inputFile.readline()

node_map = {}

while True:
    line = inputFile.readline()
    if not line:
        break

    m = re.match(r'([A-Z0-9]+) = \(([A-Z0-9]+), ([A-Z0-9]+)\)', line)
    if not m:
        break

    name = m.group(1)
    left = m.group(2)
    right = m.group(3)

    node_map[name] = {
        'L': left,
        'R': right
    }

inputFile.close()

print(f'Node map: {node_map}')


# cur_nodes = []
# for node in node_map.keys():
#     if (node[2] == 'A'):
#         cur_nodes.append(node)

cur_nodes = ['GNA', 'FCA', 'AAA', 'MXA', 'VVA', 'XHA']
# cur_nodes = ['AAA']

print(f'Starting nodes: {cur_nodes}')
print(f'Num turns: {len(turns)}')

def zedHash(node, i):
    return f'{node}-{i}'

def getTracks(node):
    i = 0
    steps = 0
    cur_node = node

    zed_tracks = {}

    while True:
        # Move to next node
        cur_node = node_map[cur_node][turns[i]]
        steps += 1

        zed_done = False

        if cur_node[2] == 'Z':
            hash = zedHash(node, i)
            if hash in zed_tracks:
                start = zed_tracks[hash]
                diff = steps - start
                break
            else:
                print(hash)
                zed_tracks[hash] = steps

        i += 1
        if i >= len(turns):
            i = 0

    # print(f'Zed tracks for {node}: ' + str(zed_tracks))
    print(f'{node}: Start: {start}, Diff: {diff}')

    return (start, diff)

diffs = []

for node in cur_nodes:
    (start, diff) = getTracks(node)
    diffs.append(diff)

lcm = numpy.lcm.reduce(diffs)

print(f'Least common multiple: {lcm}')