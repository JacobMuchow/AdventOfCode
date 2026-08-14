import os

from solutions.solution import Solution
from solutions.legacy_script import LegacyScriptSolution
from solutions.day01.day01pt1 import Day01Pt1Solution
from solutions.day01.day01pt2 import Day01Pt2Solution
from solutions.day02.day02pt1 import Day02Pt1Solution
from solutions.day10.Day10Pt1 import Day10Pt1Solution
from solutions.day10.Day10Pt2 import Day10Pt2Solution

SOLUTIONS_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCES_DIR = os.path.join(os.path.dirname(SOLUTIONS_DIR), "resources")

solution_map: dict[str, Solution] = {
    "day01pt1": Day01Pt1Solution(),
    "day01pt2": Day01Pt2Solution(),
    "day02pt1": Day02Pt1Solution(),
    "day10pt1": Day10Pt1Solution(),
    "day10pt2": Day10Pt2Solution()
}

def find_legacy_solution(day: str, part: str) -> LegacyScriptSolution | None:
    """Locate an unmigrated script, e.g. solutions/day07/pt1.py.

    Also covers the alternate-attempt files like pt1.2.py and pt2.1.py,
    since those arrive here as part="pt1.2" / "pt2.1".
    """
    script_path = os.path.join(SOLUTIONS_DIR, day, f"{part}.py")
    resource_dir = os.path.join(RESOURCES_DIR, day)
    if not os.path.isfile(script_path) or not os.path.isdir(resource_dir):
        return None
    return LegacyScriptSolution(script_path, resource_dir)

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
            return

        # Fall back to the original self-contained script, run as-is.
        legacy = find_legacy_solution(day, part)
        if legacy:
            print(f"Running legacy solution for {day} {part}")
            legacy.run()
            return

        raise ValueError(f"No solution found for {day} {part}")