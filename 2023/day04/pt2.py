import re

inputFile = open('input.txt', 'r')
copies = {}
originals = []

while True:
    line = inputFile.readline()
    if not line:
        break

    splits = re.split(r'[\:\|]', line)
    print(str(splits))

    card_id = re.match(r'Card([ ]+)([0-9]+)', splits[0]).group(2)
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

    print('Card ' + card_id)
    print('Match total: ' + str(match_total))

    originals.append(card_id)

    multiplier = 1
    if card_id in copies:
        multiplier += copies[card_id]

    for i in range(0, match_total):
        x = str(int(card_id) + 1 + i)

        if not x in copies:
            copies[x] = 0
        copies[x] += multiplier

print('Originals: ' + str(originals))
print('Copies: ' + str(copies))

total_cards = 0

for i in range(0, len(originals)):
    card_id = originals[i]

    num_copies = 0
    if card_id in copies:
        num_copies = copies[card_id]

    print(f'Card {card_id}: copies = {num_copies}')

    total_cards += 1 + num_copies

print("Total Cards: " + str(total_cards))
inputFile.close()