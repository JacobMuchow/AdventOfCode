import re
import math

inputFile = open('input.txt', 'r')

def parseNumbers(line):
    seeds = re.findall(r'([0-9]+)', line)
    return list(map(lambda seed: int(seed), seeds))

def moveToTag(file, tag):
    while True:
       line = file.readline()
       if line == None:
           return
       if line.startswith(tag):
           return
       
def parseNumberGroups(file, tag):
    groups = []
    moveToTag(file, tag)

    while True:
        line = inputFile.readline()
        if not line:
            return groups

        numbers = parseNumbers(line)
        if len(numbers) == 0:
            return groups

        # sorted()

        groups.append(numbers)

def mapping(groups, input):
    for group in groups:
        out_x = group[0]
        inp_x = group[1]
        range = group[2]
        
        inp_y = inp_x + range - 1

        if input >= inp_x and input <= inp_y:
            return out_x + (input - inp_x)
        
    return input

line = inputFile.readline()
seeds = parseNumbers(line)

map1 = parseNumberGroups(inputFile, "seed-to-soil")
map2 = parseNumberGroups(inputFile, "soil-to-fertilizer")
map3 = parseNumberGroups(inputFile, "fertilizer-to-water")
map4 = parseNumberGroups(inputFile, "water-to-light")
map5 = parseNumberGroups(inputFile, "light-to-temperature")
map6 = parseNumberGroups(inputFile, "temperature-to-humidity")
map7 = parseNumberGroups(inputFile, "humidity-to-location")

out_map = {}

def mapSeed(seed):
    if seed in out_map:
        return out_map[seed]
    
    out = mapping(map1, seed)
    out = mapping(map2, out)
    out = mapping(map3, out)
    out = mapping(map4, out)
    out = mapping(map5, out)
    out = mapping(map6, out)
    out = mapping(map7, out)

    out_map[seed] = out
    return out

def find_edge(x, y):
    print('find_edge')

    if y-x == mapSeed(y) - mapSeed(x):
        return y

    left = x
    right = y

    loop_count = 0

    while True:
        loop_count += 1

        # Edge found
        if right-left <= 1:
            return left
        
        i = left + int((right-left) / 2)

        if i - x == mapSeed(i) - mapSeed(x):
            left = i
        else:
            right = i

outputs = []
test_seeds = []

si = 0
while si < len(seeds):
    x = seeds[si]
    y = seeds[si] + seeds[si+1] - 1

    test_seeds.append(x)

    while x < y:
        edge = find_edge(x, y)
        if edge == y:
            break
        
        x = edge + 1
        test_seeds.append(x)

    si += 2

print(f'Seeds: {test_seeds}')


outputs = list(map(lambda seed: mapSeed(seed), test_seeds))

min_out = min(outputs)
print('Min: ' + str(min_out))

inputFile.close()