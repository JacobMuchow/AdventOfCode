import sys
import time

from solutions.solution_runner import SolutionRunner

if len(sys.argv) < 2:
    print("Usage: python main.py <day> <part>")
    print("Ex) python main.py 14 pt1")
    sys.exit(1)

day = sys.argv[1]
part = sys.argv[2]

start = time.time()
SolutionRunner.run(day, part)
end = time.time()

time_taken_ms = (end - start) * 1000
print(f"Time taken: {time_taken_ms} ms")