import re
import math

inputFile = open('input.txt', 'r')

times_raw = inputFile.readline()
distances_raw = inputFile.readline()

inputFile.close()

times = re.findall(r'([0-9]+)', times_raw)
distances = re.findall(r'([0-9]+)', distances_raw)

print('Times: ' + str(times))
print('Distances: ' + str(distances))

def distanceForTimeCharge(timeCharge, totalTime):
    speed = timeCharge
    time_left = totalTime - timeCharge

    return speed * time_left

def findBoundX(time, record):
    x = 1
    y = time-1

    left = x
    right = y

    while True:
        if right-left <= 1:
            return left + 1
        
        i = left + int((right-left) / 2)

        if distanceForTimeCharge(i, time) <= record:
            left = i
        else:
            right = i

def findBoundY(time, record):
    x = 1
    y = time-1

    left = x
    right = y

    while True:
        if right-left <= 1:
            return left
        
        i = left + int((right-left) / 2)

        if distanceForTimeCharge(i, time) > record:
            left = i
        else:
            right = i


def newRecordTimes(time, record):
    x = findBoundX(time, record)
    y = findBoundY(time, record)

    return (x, y)

time = times[0]
record = distances[0]

print(f'Time: {time}, Record: {record}')

(x, y) = newRecordTimes(int(time), int(record))
print(f'Bounds: {x}, {y}')

ways = y - x + 1
print(f'Ways: {ways}')