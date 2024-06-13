import re

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

    m = re.match(r'([A-Z]+) = \(([A-Z]+), ([A-Z]+)\)', line)
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

i = 0
steps = 0
cur_node = 'AAA'

while cur_node != 'ZZZ':
    turn = turns[i]
    cur_node = node_map[cur_node][turn]

    i += 1
    if i >= len(turns):
        i = 0

    steps += 1

print('Found ZZZ')
print(f'Total steps: {steps}')