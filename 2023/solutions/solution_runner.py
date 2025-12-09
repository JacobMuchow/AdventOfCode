from solutions.solution import Solution
from solutions.day01.day01pt1 import Day01Pt1Solution
from solutions.day01.day01pt2 import Day01Pt2Solution
from solutions.day02.day02pt1 import Day02Pt1Solution
from solutions.day10.Day10Pt1 import Day10Pt1Solution
from solutions.day10.Day10Pt2 import Day10Pt2Solution

solution_map: dict[str, Solution] = {
    "day01pt1": Day01Pt1Solution(),
    "day01pt2": Day01Pt2Solution(),
    "day02pt1": Day02Pt1Solution(),
    "day10pt1": Day10Pt1Solution(),
    "day10pt2": Day10Pt2Solution()
}

class SolutionRunner:
    @staticmethod
    def run(day: str, part: str) -> Solution:
        # Handle variety of formats for day param. E.g., "1", "day1", "day01"
        if day.startswith("day"):
            day = day.removeprefix("day")
        if len(day) == 1:
            day = "0" + day
        day = f"day{day}"

        # Same for part param. E.g., "1", "pt1"
        if not part.startswith("pt"):
            part = "pt" + part

        key = f"{day}{part}"
        if key in solution_map:
            print(f"Running solution for {day} {part}")
            solution_map[key].run()
        else:
            raise ValueError(f"No solution found for {day} {part}")