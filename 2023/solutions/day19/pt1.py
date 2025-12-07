import re
import sys
from pprint import pprint

sys.setrecursionlimit(1000000)

inputFile = open('input.txt', 'r')

workflows = {}
parts = []

# Parse workflows
while True:
    line = inputFile.readline()
    if not line:
        break

    # print(line)
    match = re.match(r'([A-Za-z]+)\{(.*)\}', line)
    if not match:
        break
    name = match[1]
    rules_raw = match[2].split(',')

    default = rules_raw.pop()
    rules = []

    for rule_raw in rules_raw:
        match = re.match(r'([A-Za-z]+)([<>])([0-9]+):([A-Za-z]+)', rule_raw)
        rules.append({
            'prop': match[1],
            'sign': match[2],
            'value': int(match[3]),
            'dest': match[4]
        })

    workflows[name] = {
        'rules': rules,
        'default': default
    }

# Parse machine parts
while True:
    line = inputFile.readline()
    if not line:
        break

    match = re.match(r'\{x=([0-9]+),m=([0-9]+),a=([0-9]+),s=([0-9]+)\}', line)
    parts.append({
        'x': int(match[1]),
        'm': int(match[2]),
        'a': int(match[3]),
        's': int(match[4])
    })

accepted_parts = []

def satisfies_rule(part: dict, rule: dict) -> bool:
    if rule['sign'] == '>':
        return part[rule['prop']] > rule['value']
    else:
        return part[rule['prop']] < rule['value']


for part in parts:
    workflow = workflows['in']
    
    while True:
        dest = workflow['default']

        for rule in workflow['rules']:
            if satisfies_rule(part, rule):
                dest = rule['dest']
                break

        if dest == 'A':
            accepted_parts.append(part)
            break
        if dest == 'R':
            break

        workflow = workflows[dest]

print('Accepted parts: ' + str(accepted_parts))

total = 0
for part in accepted_parts:
    total += part['x'] + part['m'] + part['a'] + part['s']

print(f'Total: {total}')

inputFile.close()

