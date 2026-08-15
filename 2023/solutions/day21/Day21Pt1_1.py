from dataclasses import dataclass
from enum import Enum

from solutions.solution import Solution
from utils.files import FileUtils

STEP_GOAL = 64

@dataclass
class Pos2D:
    x: int
    y: int

    def __str__(self):
        return f"{self.x},{self.y}"

    def key(self) -> str:
        return f"{self.x},{self.y}"

class Polarity(Enum):
    Even = 0
    Odd = 1

    def __str__(self):
        return "Even" if self == Polarity.Even else "Odd"

    @classmethod
    def of(cls, val: int) -> "Polarity":
        return Polarity.Even if val % 2 == 0 else Polarity.Odd

    def flip(self) -> "Polarity":
        return Polarity.Odd if self == Polarity.Even else Polarity.Even

@dataclass
class QueueItem:
    pos: Pos2D
    polarity: Polarity
    step: int

class Day21Pt1_1Solution(Solution):
    grid: list[str]

    def run(self) -> None:
        self.grid = FileUtils.read_lines('resources/day21/input.txt')
        for line in self.grid:
            print(line)

        start = self._find_start()
        print(f"Start: {start}")

        # Assign start '.' value so later comparisons are easier
        self.grid[start.y] = self.grid[start.y].replace('S', '.', 1)

        # Set up optimized search queue
        queue: list[QueueItem] = [QueueItem(start, Polarity.Even, step=0)]
        seen: set[str] = set()
        goal_polarity = Polarity.of(STEP_GOAL)
        end_count = 0

        # process queue
        while len(queue) > 0:
            item = queue.pop(0)
            pos = item.pos

            # Validate pos
            if pos.y < 0 or pos.y >= len(self.grid): continue
            if pos.x < 0 or pos.x >= len(self.grid[0]): continue
            if self.grid[pos.y][pos.x] == '#': continue

            # Skip seen, else add to seen
            if pos.key() in seen: continue
            seen.add(pos.key())

            # If the step goal is even, and the current step is even, we know we can always end up on this tile
            # Vice versa for odd/odd.
            # The pos is already stored in seen, so it only gets counted once.
            if item.polarity == goal_polarity:
                end_count += 1

            # Don't proceed past the step goal
            if item.step >= STEP_GOAL:
                continue

            # Enqueue future step possibilities. 
            # Guard on popping the item covers out-of-bounds and invalid tiles.
            next_polarity = item.polarity.flip()
            next_step = item.step + 1

            queue.append(QueueItem(Pos2D(pos.x-1, pos.y), next_polarity, next_step))
            queue.append(QueueItem(Pos2D(pos.x+1, pos.y), next_polarity, next_step))
            queue.append(QueueItem(Pos2D(pos.x, pos.y-1), next_polarity, next_step))
            queue.append(QueueItem(Pos2D(pos.x, pos.y+1), next_polarity, next_step))

        print(f"Num possibilities: {end_count}")


    def _find_start(self) -> Pos2D:
        for y in range(0, len(self.grid)):
            row = self.grid[y]
            for x in range(0, len(row)):
                if row[x] == 'S':
                    return Pos2D(x, y)
        raise RuntimeError('Starting pos not found')