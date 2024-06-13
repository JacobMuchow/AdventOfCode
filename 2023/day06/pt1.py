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

def newRecordTimes(time, record):
    bound_x = 1
    bound_y = time-1

    while bound_x < bound_y:
        if distanceForTimeCharge(bound_x, time) > record:
            break
        bound_x += 1

    while bound_y > bound_x:
        if distanceForTimeCharge(bound_y, time) > record:
            break
        bound_y -= 1

    return (bound_x, bound_y)

combinations = 1

for i in range(0, len(times)):
    time = times[i]
    record = distances[i]

    (x, y) = newRecordTimes(int(time), int(record))
    print(f'Time: {time}, Record: {record}. Bounds: {x}, {y}')

    combinations *= y - x + 1

print(f'Totals: {combinations}')