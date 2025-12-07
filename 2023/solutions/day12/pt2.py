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
    
    line_raw = match[1]
    blocks_raw = match[2]

    # lines.append(line_raw)

    blocks = re.findall(r'([0-9]+)', blocks_raw)
    blocks = list(map(lambda x: int(x), blocks))
    # dmg_chunks.append(blocks)

    # "Unfolding"
    line = ""
    for i in range(0, 4):
        line += line_raw + "?"
    line += line_raw

    out_blocks = []
    for i in range(0, 5):
        out_blocks += blocks

    lines.append(line)
    dmg_chunks.append(out_blocks)

inputFile.close()

print(str(lines))
print(str(dmg_chunks))

def memoize(func):
    records = {}

    def wrapped(*args):
        key = str(args)
        # print('Key: ' + key)
        if key in records:
            # print('Record found')
            return records[key]
        
        result = func(*args)
        records[key] = result
        return result
    
    return wrapped

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

def findSolnsRecursive(line: str, chunks: list):
    debugPrint(f'findSolnRecursive {line} {chunks}')

    solns = 0

    for x in range(0, len(line)):
        prev_line = line[0:x]
        debugPrint(f'Prev line: {prev_line}')
        if prev_line.find('#') >= 0:
            debugPrint('Found #, break;')
            break

        chunk_fits = chunkFits(line, x, chunks[0])
        debugPrint(f'Chunk fits: {x} {chunk_fits}')
        
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
            new_solns = lineSolns(new_line, new_chunks)
            if new_solns > 0:
                solns += new_solns
                debugPrint(f'Solns: {solns}')
            
    return solns

lineSolns = memoize(findSolnsRecursive)

# solns = lineSolns(lines[5], dmg_chunks[5])
# print(f'{lines[5]} - {solns}')

all_solns = []
for i in range(0, len(lines)):
    solns = lineSolns(lines[i], dmg_chunks[i])
    all_solns.append(solns)

totals = 0
for soln in all_solns:
    totals += soln

print(f'Totals: {totals}')

# lines_unfolded = lines.copy()
# chunks_unfolded = dmg_chunks.copy()

# def unfold(lines_in, chunks_in):
#     lines_out = []
#     for i in range(0, len(lines_in)):
#         lines_out.append(lines_in[i] + "?" + lines[i])

#     chunks_out = []
#     for i in range(0, len(chunks_in)):
#         chunks_out.append(chunks_in[i] + dmg_chunks[i])

#     return (lines_out, chunks_out)

# for i in range (0, 4):
#     (lines_unfolded, chunks_unfolded) = unfold(lines_unfolded, chunks_unfolded)

#     for i in range(0, len(lines_unfolded)):
#         solns = lineSolns(lines_unfolded[i], chunks_unfolded[i])
#         all_solns[i].append(solns)

# factors = []
# for i in range(0, len(all_solns)):
#     print(f'"{lines[i]} - {all_solns[i]}"')
#     factor = all_solns[i][1] / all_solns[i][0]
#     factors.append(factor)

# print(f'Factors: {factors}')

# solns_unfolfed = []
# for i in range(0, len(factors)):
#     soln = pow(factors[i], 4) * all_solns[i][0]
#     solns_unfolfed.append(soln)

# print(f'Solns: {solns_unfolfed}')

# totals = 0
# for soln in solns_unfolfed:
#     totals += soln

# print(f'Totals: {totals}')
    

# lines2 = []
# for line in lines:
#     lines2.append(line + "?" + line)

# chunks2 = []
# for chunk in dmg_chunks:
#     chunks2.append(chunk + chunk)

# solns2 = []
# for i in range(0, len(lines2)):
#     solns = lineSolns(lines2[i], chunks2[i])
#     print(f'{lines2[i]} - {solns}')
#     solns2.append(solns)

# totals = 0

# for i in range(0, len(solns1)):
#     factor = solns2[i] / solns1[i]
#     print(f'{lines[i]} {solns1[i]} {solns2[i]} - factor {factor}')

#     real_soln = pow(factor, 5)
#     print(f'{real_soln}')
#     totals += real_soln

# print(f'Totals: {totals}')