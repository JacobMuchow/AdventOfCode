import re

inputFile = open('input.txt', 'r')
sum = 0

def parseGameId(line):
    m = re.search(r'Game ([0-9]+): ', line)
    if not m:
        return None
    return m.group(1)

def parseColor(raw, color):
    m = re.search(f'([0-9]*) {color}', raw)
    if not m:
        return 0
    return int(m.group(1))

def parseSet(raw):
    red = parseColor(raw, 'red')
    green = parseColor(raw, 'green')
    blue = parseColor(raw, 'blue')

    # print('Raw: ' + raw)
    # print(f'R: {red}, G: {green}, B: {blue}')

    return (red, green, blue)

# MAX_RED = 12
# MAX_GREEN = 13
# MAX_BLUE = 14

# possible_games = []

power = 0
 
while True:
    line = inputFile.readline()

    id = parseGameId(line)
    if not id:
        # EOF
        break

    sets_raw = re.split(';', line)
    possible = True

    min_red = 0
    min_green = 0
    min_blue = 0

    for set_raw in sets_raw:
        (red, green, blue) = parseSet(set_raw)

        if red > min_red:
            min_red = red

        if green > min_green:
            min_green = green

        if blue > min_blue:
            min_blue = blue
        
        # if red > MAX_RED or green > MAX_GREEN or blue > MAX_BLUE:
        #     possible = False
        #     break
            
    print('Min: ' + str((min_red, min_green, min_blue)))

    power += min_red * min_green * min_blue

    # if possible:
    #     possible_games.append(id)

print("Power: " + str(power))

# print('Games: ' + str(possible_games))

# sum = 0
# for game in possible_games:
#     sum += int(game)    

# print("Sum: " + str(sum))
# inputFile.close()