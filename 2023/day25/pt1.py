import re
import sys
from pprint import pprint
from copy import deepcopy
import numpy as np

sys.setrecursionlimit(1000000)

inputFile = open('test.txt', 'r')

class Node:
    def __init__(self, name: str) -> None:
        self.name = name
        self.neighbors = {}

    def __str__(self) -> str:
        return f'{self.name}: ' + ", ".join(self.neighbors.keys())

node_map = {}

def findOrCreate(name: str) -> Node:
    global node_map

    if not name in node_map:
        node_map[name] = Node(name)

    return node_map[name]


# Parse stones
while True:
    line = inputFile.readline()
    if not line:
        break

    tokens = re.findall(r'[a-z]+', line)
    node_name = tokens[0]

    node = findOrCreate(node_name)

    for i in range(1, len(tokens)):
        name_i = tokens[i]
        node_i = findOrCreate(name_i)

        node_i.neighbors[node_name] = node
        node.neighbors[name_i] = node_i

inputFile.close()

for n in node_map:
    print(node_map[n])