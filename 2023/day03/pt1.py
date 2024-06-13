import re

inputFile = open('test.txt', 'r')
lines = []
symbols = []

while True:
    line = inputFile.readline()
    if not line:
        break

    lines.append(line)

for y in range(0, len(lines)):
    line = lines[y]

    print(line)

    iter = re.finditer(r'([0-9]+)', line)
    for m in iter:
        print(f'{m.group(0)}: {m.start()}, {m.end()}')

        roi_x_min = max(m.start()-1, 0)
        roi_x_max = min(m.end(), len(line)-1)

        roi_y_min = max(y-1, 0)
        roi_y_max = min(y+1, len(lines)-1)

        roi = ((roi_x_min, roi_y_min), (roi_x_max, roi_y_max))
        print('roi: ' + str(roi))

        symbol = False
        ignore_map = {
            '0': True,
            '1': True,
            '2': True,
            '3': True,
            '4': True,
            '5': True,
            '6': True,
            '7': True,
            '8': True,
            '9': True,
            '.': True,
            '\n': True
        }

        for roi_y in range(roi_y_min, roi_y_max+1):
            for roi_x in range(roi_x_min, roi_x_max+1):
                if ignore_map.get(lines[roi_y][roi_x]):
                    continue
                symbol = True
                break

            if symbol:
                break

        if symbol:
            symbols.append(m.group(0))

print("Symbols: " + str(symbols))
inputFile.close()

sum = 0
for symbol in symbols:
    sum += int(symbol)

print("Sum: " + str(sum))