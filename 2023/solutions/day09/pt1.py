import re

inputFile = open('input.txt', 'r')
originals = []

while True:
    line = inputFile.readline()
    if not line:
        break
    
    inputs = re.findall(r'([\-0-9]+)', line)
    numbers = list(map(lambda input: int(input), inputs))
    originals.append(numbers)

# ignore
inputFile.readline()

def getDiffs(seq):
    all_zero = True
    diffs = []

    for i in range(1, len(seq)):
        diff = seq[i] - seq[i-1]
        diffs.append(diff)
        if diff != 0:
            all_zero = False

    return (diffs, all_zero)

def loopDiffs(originalSeq):
    seqs = [originalSeq]
    seqCount = 1
    all_zero = False

    while not all_zero:
        (seq, all_zero) = getDiffs(seqs[seqCount-1])
        seqs.append(seq)
        seqCount += 1

    return seqs

def findNext(sequence):
    seqs = loopDiffs(sequence)
    carry = 0

    # for seq in seqs:
    #     print(str(seq))

    y = len(seqs)-2

    while y >= 0:
        seq = seqs[y]
        count = len(seq)

        carry += seq[count-1]
        # print('Carry: ' + str(carry))

        y -= 1

    return carry

# seq = originals[2]
# seq.reverse()
# findNext(seq)

results = []

for seq in originals:
    seq.reverse()
    results.append(findNext(seq))

total = 0
for result in results:
    print(str(result))
    total += result

print('Total: ' + str(total))