import re
import math

hands = []
bid_map = {}

inputFile = open('input.txt', 'r')

card_values = {
    'A': 14,
    'K': 13,
    'Q': 12,
    'J': 11,
    'T': 10,
    '9': 9,
    '8': 8,
    '7': 7,
    '6': 6,
    '5': 5,
    '4': 4,
    '3': 3,
    '2': 2,
}

while True:
    line = inputFile.readline()
    if not line:
        break

    m = re.match(r'([AKQJT98765432]+) ([0-9]+)', line)
    if not m:
        break

    hands.append(m.group(1))
    bid_map[m.group(1)] = int(m.group(2))

inputFile.close()

rank_cache = {}

def rankHand(hand):
    if hand in rank_cache:
        return rank_cache[hand]
    
    # Count appearances of all cards
    card_map = {}
    for i in range(0, len(hand)):
        card = hand[i]
        if card in card_map:
            card_map[card] += 1
        else:
            card_map[card] = 1

    def _rank(card_map):
        # Get most repeated card
        keys = list(card_map)
        key_count = len(keys)

        if key_count == 1:
            # 5 of a kind
            return 7
        
        if key_count == 2:
            # 4 of kind or full house
            if card_map[keys[0]] == 4 or card_map[keys[0]] == 1:
                return 6
            else:
                return 5

        if key_count == 3:
            # 3 of a kind or two pair
            for key in keys:
                if card_map[key] == 3:
                    return 4
                if card_map[key] == 2:
                    return 3
                
            raise f'Error: this should not have been possible. card_map: {card_map}'
        
        if key_count == 4:
            # pair
            return 2
        
        if key_count == 5:
            # high card
            return 1
        
        raise f'Error: unexpected key count ({key_count})'
    
    rank = _rank(card_map)
    rank_cache[hand] = rank
    return rank

def rankV2(hand):
    rank = rankHand(hand)
    return (rank, card_values[hand[0]], card_values[hand[1]], card_values[hand[2]], card_values[hand[3]], card_values[hand[4]])


def compareHands(hand_l, hand_r):
    rank_l = rankHand(hand_l)
    rank_r = rankHand(hand_r)

    if rank_l != rank_r:
        return rank_r - rank_l
    
    for i in range(0, 5):
        card_l = hand_l[i]
        card_r = hand_r[i]

        if card_l != card_r:
            return card_values[card_r] - card_values[card_l]
    
    return 0
            
hands_sorted = sorted(hands, key=rankV2)

winnings = 0

for i in range(0, len(hands_sorted)):
    hand = hands_sorted[i]
    winnings += bid_map[hand] * (i+1)

print(f"Winnings: {winnings}")
print("Done")