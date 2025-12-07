import re
import sys
from copy import deepcopy
from pprint import pprint

sys.setrecursionlimit(1000000)

inputFile = open('input.txt', 'r')

workflows = {}

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

x = 1
min_val = 1
max_val = 4000

segment_queue = [{
    'workflow': 'in',
    'x': [1,4000],
    'm': [1,4000],
    'a': [1,4000],
    's': [1,4000]
}]

def satisfiesRule(segment: dict, rule: dict):
    if rule['sign'] == '<':
        if segment[rule['prop']][1] < rule['value']:
            return True
    else:
        if segment[rule['prop']][0] > rule['value']:
            return True
        
def splitToSatisfyRule(segment: dict, rule: dict):
    good_seg = deepcopy(segment)
    bad_seg = deepcopy(segment)

    if rule['sign'] == '<':
        # No chunck of the segment can satisfy the rule
        if segment[rule['prop']][0] >= rule['value']:
            return None
        
        # Split into good & bad segs
        good_seg[rule['prop']][1] = rule['value'] - 1
        good_seg['workflow'] = rule['dest']

        bad_seg[rule['prop']][0] = rule['value']
    else:
        # No chunck of the segment can satisfy the rule
        if segment[rule['prop']][1] <= rule['value']:
            return None

        # Split into good & bad segs
        good_seg[rule['prop']][0] = rule['value'] + 1
        good_seg['workflow'] = rule['dest']

        bad_seg[rule['prop']][1] = rule['value']
    
    return (good_seg, bad_seg)
        

accepted_segments = []

while len(segment_queue) > 0:
    # print(f'Queue: {len(segment_queue)}')
    # for item in segment_queue:
    #     pprint(item)
    # print("\n")

    segment = segment_queue.pop(0)

    if segment['workflow'] == 'A':
        # print('Segment accepted')
        accepted_segments.append(segment)
        continue
    if segment['workflow'] == 'R':
        # print('Segment rejected')
        continue

    workflow = workflows[segment['workflow']]
    action_taken = False

    for rule in workflow['rules']:
        # Entire segment fits in rule
        if satisfiesRule(segment, rule):
            action_taken = True
            dest = rule['dest']

            # print(f'Moving segment to "{dest}"')
            segment['workflow'] = dest
            segment_queue.insert(0, segment)
            break
            
        else:
            # Determine if this segment can be split to satisfy the rule.
            new_segs = splitToSatisfyRule(segment, rule)

            # Cannot split, move to next rule
            if new_segs is None:
                # print('Next rule')
                continue

            # Evaluate our new segments
            # print('Splitting segments')
            segment_queue.insert(0, new_segs[1])
            segment_queue.insert(0, new_segs[0])
            action_taken = True
            break

    if not action_taken:
        default = workflow['default']
        # print(f'Moving segment to Default: "{default}"')
        segment['workflow'] = default
        segment_queue.insert(0, segment)

# print('FINISHED')
# print(f'Segments: {len(accepted_segments)}')

total = 0

for segment in accepted_segments:
    # pprint(segment)
    # print()

    s = segment['s'][1] - segment['s'][0] + 1
    m = segment['m'][1] - segment['m'][0] + 1
    a = segment['a'][1] - segment['a'][0] + 1
    x = segment['x'][1] - segment['x'][0] + 1

    total += s * m * a * x

print(f'Total: {total}')

