import re
import sys

# sys.setrecursionlimit(1_000_000)

inputFile = open('input.txt', 'r')
lines = []
dmg_chunks = []

# Read lines
while True:
    line = inputFile.readline()
    if not line:
        break
    match = re.match(r'(.*) (.*)', line)
    
    lines.append(match[1])
    blocks_raw = match[2]

    # segments = []
    # it = re.finditer(r'(.)\1{0,}', segments_raw)
    # for match in it:
    #     segments.append(match[0])

    # print(str(segments))

    blocks = re.findall(r'([0-9]+)', blocks_raw)
    blocks = list(map(lambda x: int(x), blocks))
    dmg_chunks.append(blocks)

inputFile.close()

print(str(lines))
print(str(dmg_chunks))

def chunkFits(line, x, chunk):
    # out of bounds
    if x + chunk > len(line):
        return False
    
    # if chunck
    if x > 0 and line[x-1] == '#':
        return False
    
    # Returns false if segment is not long enough
    for x2 in range(x, x+chunk):
        if line[x2] == '.':
            return False
        
    # Returns false if chunk is for sure too long
    if x+chunk < len(line) and line[x+chunk] == '#':
        return False
        
    return True

def debugPrint(text: str):
    if False:
        print(text)

def findSolnsRecursive(line: str, chunks: list, depth: int):
    debugPrint(f'({depth}) findSolnRecursive {line} {chunks}')

    solns = 0

    for x in range(0, len(line)):
        prev_line = line[0:x]
        debugPrint(f'Prev line: {prev_line}')
        if prev_line.find('#') >= 0:
            debugPrint('Found #, break;')
            break

        chunk_fits = chunkFits(line, x, chunks[0])
        debugPrint(f'({depth}) Chunk fits: {x} {chunk_fits}')
        
        if chunk_fits:
            possible_soln = len(chunks) == 1

            # if (len(chunks)) == 1:
            #     debugPrint('Soln found')
            #     solns += 1
            #     continue

            new_x = x + chunks[0]
            # old_line = line[0:new_x]
            new_line = line[new_x:]

            if len(new_line) == 0:
                if possible_soln:
                    debugPrint('Soln found')
                    solns += 1
                continue

            if new_line[0] == '?':
                new_line = new_line[1:]
                debugPrint(f'Skip ?: "{new_line}" ({len(new_line)})')

            if len(new_line) == 0:
                if possible_soln:
                    debugPrint('Soln found')
                    solns += 1
                continue

            if possible_soln:
                invalid = False
                for i in range(0, len(new_line)):
                    if new_line[i] == '#':
                        invalid = True
                        break
                if not invalid:
                    debugPrint('Soln found')
                    solns += 1
                continue

            new_chunks = chunks.copy()
            new_chunks.pop(0)
            new_solns = findSolnsRecursive(new_line, new_chunks, depth+1)
            if new_solns > 0:
                solns += new_solns
                debugPrint(f'Solns: {solns}')
            
    return solns


def lineSolns(line, chunks):
    return findSolnsRecursive(line, chunks, 0)

# solns = lineSolns(lines[5], dmg_chunks[5])
# print(f'{lines[5]} - {solns}')

total_solns = 0

for i in range(0, len(lines)):
    solns = lineSolns(lines[i], dmg_chunks[i])
    print(f'{lines[i]} - {solns}')
    total_solns += solns

print('Total solns: ' + str(total_solns))