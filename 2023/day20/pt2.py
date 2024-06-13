import re
import sys
from pprint import pprint
from copy import deepcopy
import math

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

def pushButton():
    global modules
    global conjuctions
    global button_presses
    signal_queue = []

    broadcaster = modules['broadcaster']
    for output in broadcaster['outputs']:
        signal_queue.append({
            'name': output,
            'pulse': 'low',
            'source': 'broadcaster'
        })
        
    while len(signal_queue) > 0:
        signal = signal_queue.pop(0)

        if signal['name'] == 'rx' and signal['pulse'] == 'low':
            return True

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

            if next_pulse == 'high' and module['name'] in conjuctions:
                cycle_lengths.append(button_presses)
                conjuctions.remove(module['name'])

        if next_pulse is not None:
            for output in module['outputs']:
                signal_queue.append({
                    'name': output,
                    'pulse': next_pulse,
                    'source': module['name']
                })

    return False

conjuctions = []
cycle_lengths = []

for name in modules:
    if 'rx' in modules[name]['outputs']:
        for out in modules[name]['last']:
            conjuctions.append(out)
        break

print(str(conjuctions))

button_presses = 0

while True:
    button_presses += 1
    if button_presses % 1000 == 0:
        print(f'Press: {button_presses}')
    if pushButton():
        break

    if len(conjuctions) == 0:
        break

print(f'Button presses: {button_presses}')
print(f'Cycle lenghts: {cycle_lengths}')

lcm = math.lcm(*cycle_lengths)
print(f'LCM: {lcm}')