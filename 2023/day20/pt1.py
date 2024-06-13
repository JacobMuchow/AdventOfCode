import re
import sys
from pprint import pprint
from copy import deepcopy

sys.setrecursionlimit(1000000)

inputFile = open('input.txt', 'r')

modules = {}

# Parse workflows
while True:
    line = inputFile.readline()
    if not line:
        break

    # print(line)
    token = line.split(' -> ')
    module_raw = token[0]
    outputs = re.findall(r'([a-z]+)', token[1])

    type = None

    if module_raw[0] == '%' or module_raw[0] == '&':
        type = module_raw[0]
        name = module_raw[1:]
    else:
        name = module_raw

    modules[name] = {
        'name': name,
        'type': type,
        'outputs': outputs
    }

    if type == '%':
        modules[name]['state'] = 'off'
    if type == '&':
        modules[name]['last'] = {}

inputFile.close()

for name in modules:
    m1 = modules[name]

    for output in m1['outputs']:
        if output in modules:
            m2 = modules[output]
            if m2['type'] == '&':
                m2['last'][m1['name']] = 'low'

def pushButton(modules):
    modules = deepcopy(modules)
    signal_queue = []
    low_count = 1
    high_count = 0

    broadcaster = modules['broadcaster']
    for output in broadcaster['outputs']:
        signal_queue.append({
            'name': output,
            'pulse': 'low',
            'source': 'broadcaster'
        })
        
    while len(signal_queue) > 0:
        signal = signal_queue.pop(0)
        # print(f"{signal['source']} -{signal['pulse']}-> {signal['name']}")
        
        if signal['pulse'] == 'high':
            high_count += 1
        else:
            low_count += 1

        if not signal['name'] in modules:
            continue

        module = modules[signal['name']]
        
        next_pulse = None

        if module['type'] == '%':
            if signal['pulse'] == 'low':
                module['state'] = 'on' if module['state'] == 'off' else 'off'
                next_pulse = 'high' if module['state'] == 'on' else 'low'

        if module['type'] == '&':
            module['last'][signal['source']] = signal['pulse']

            all_high = True
            for name in module['last']:
                if module['last'][name] == 'low':
                    all_high = False
                    break

            next_pulse = 'low' if all_high else 'high'

        if next_pulse is not None:
            for output in module['outputs']:
                signal_queue.append({
                    'name': output,
                    'pulse': next_pulse,
                    'source': module['name']
                })

    return (low_count, high_count, modules)

def stateKey(modules: dict) -> str:
    return str(modules)

state_memo = {}
total_low = 0
total_high = 0

# 4 Cycle = 17,11
did_print = False

for i in range(0, 1000):
    key = stateKey(modules)

    if not key in state_memo:
        (low_count, high_count, modules) = pushButton(modules)
        state_memo[key] = (low_count, high_count, modules)
    else:
        print('Hit')

    (low_count, high_count, modules) = state_memo[key]
    # print(f'{i}: low: {low_count}, high: {high_count}')

    total_low += low_count
    total_high += high_count

print(f'Total low: {total_low}')
print(f'Total high: {total_high}')
print(f'Result: {total_high * total_low}')