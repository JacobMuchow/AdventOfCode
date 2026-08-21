import os

from solutions.solution import Solution
from solutions.legacy_script import LegacyScriptSolution
from solutions.day10.Day10Pt1 import Day10Pt1Solution
from solutions.day10.Day10Pt2 import Day10Pt2Solution
from solutions.day21.Day21Pt1_1 import Day21Pt1_1Solution
from solutions.day21.Day21Pt2_3 import Day21Pt2_3Solution
from solutions.day24.Day24Pt2_1 import Day24Pt2_1Solution

SOLUTIONS_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCES_DIR = os.path.join(os.path.dirname(SOLUTIONS_DIR), "resources")

solution_map: dict[str, Solution] = {
    # pt1 was first solved as a legacy script, so the later rewrite is the variant.
    "day10pt1.2": Day10Pt1Solution(),
    "day10pt2": Day10Pt2Solution(),
    "day21pt1.1": Day21Pt1_1Solution(),
    "day21pt2.3": Day21Pt2_3Solution(),
    "day24pt2.1": Day24Pt2_1Solution()
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