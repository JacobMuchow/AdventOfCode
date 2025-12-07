import re

inputFile = open('input.txt', 'r')
total_points = 0

while True:
    line = inputFile.readline()
    if not line:
        break

    splits = re.split(r'[\:\|]', line)
    print(str(splits))

    winning_nums = re.findall(r'([0-9]+)', splits[1])
    game_nums = re.findall(r'([0-9]+)', splits[2])

    # Faster search
    winning_map = {}
    for num in winning_nums:
        winning_map[num] = True

    match_total = 0
    for num in game_nums:
        if num in winning_map:
            match_total += 1

    points = 0 if match_total == 0 else pow(2, match_total-1)

    print('Match total: ' + str(match_total))
    print('Points: ' + str(points))

    total_points += points

print("Total points: " + str(total_points))
inputFile.close()