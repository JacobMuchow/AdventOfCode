from solutions.solution import Solution

class Day01Pt1Solution(Solution):
    def run(self) -> None:
        inputFile = open('resources/day01/input.txt', 'r')

        sum = 0

        def isNumber(char):
            uni = ord(char)
            return uni >= 48 and uni <= 57
        
        while True:
            line = inputFile.readline()
            if not line:
                break

            print(line.strip())

            x = 0
            y = len(line)-1

            valX = ''
            valY = ''

            while x <= y:
                if isNumber(line[x]):
                    valX = line[x]
                    break
                x += 1

            while y >= x:
                if isNumber(line[y]):
                    valY = line[y]
                    break
                y -= 1

            num = int(valX + valY)
            sum += num
            
        
        print("Sum: " + str(sum))
        inputFile.close()