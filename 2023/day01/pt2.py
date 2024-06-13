inputFile = open('input.txt', 'r')

sum = 0
words = [
    'one',
    'two',
    'three',
    'four',
    'five',
    'six',
    'seven',
    'eight',
    'nine'
]

mapping = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9'
}

def isNumber(char):
    uni = ord(char)
    return uni >= 48 and uni <= 57
 
while True:
    line = inputFile.readline()
    if not line:
        break

    # print(line.strip())

    x = 0
    y = len(line)-1

    valX = None
    valY = None

    while x <= y:
        if isNumber(line[x]):
            valX = line[x]
            break

        for word in words:
            x_word = 0
            x_line = x

            while True:
                if x_line >= len(line):
                    break

                if x_word >= len(word):
                    valX = mapping[word]
                    break

                if word[x_word] == line[x_line]:
                    x_word += 1
                    x_line += 1
                else:
                    break

            if valX is not None:
                break

        if valX is not None:
            break

        x += 1

    while y >= x:
        if isNumber(line[y]):
            valY = line[y]
            break

        for word in words:
            y_word = len(word)-1
            y_line = y

            while True:
                if y_line < 0:
                    break

                if y_word < 0:
                    valY = mapping[word]
                    break

                if word[y_word] == line[y_line]:
                    y_word -= 1
                    y_line -= 1
                else:
                    break

            if valY is not None:
                break

        if valY is not None:
            break

        y -= 1

    # print(valX)
    # print(valY)

    num = int(valX + valY)
    sum += num
    
 
print("Sum: " + str(sum))
inputFile.close()