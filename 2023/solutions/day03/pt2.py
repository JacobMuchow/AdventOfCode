import re

inputFile = open('input.txt', 'r')
lines = []
gear_map = {}

def xyHash(x, y):
    return f'{x},{y}'

while True:
    line = inputFile.readline()
    if not line:
        break

    lines.append(line)

for y in range(0, len(lines)):
    line = lines[y]

    iter = re.finditer(r'([0-9]+)', line)
    for m in iter:
        roi_x_min = max(m.start()-1, 0)
        roi_x_max = min(m.end(), len(line)-1)

        roi_y_min = max(y-1, 0)
        roi_y_max = min(y+1, len(lines)-1)

        for roi_y in range(roi_y_min, roi_y_max+1):
            for roi_x in range(roi_x_min, roi_x_max+1):
                if lines[roi_y][roi_x] == '*':
                    hash = xyHash(roi_x, roi_y)
                    print('Gear: ' + str(hash))

                    if hash not in gear_map:
                        gear_map[hash] = []
                        
                    gear_map[hash].append(int(m.group(0)))


print("Gear map: " + str(gear_map))
inputFile.close()

sum = 0
for key in gear_map.keys():
    symbols = gear_map[key]
    if (len(symbols) == 2):
        sum += symbols[0] * symbols[1]

print("Sum: " + str(sum))