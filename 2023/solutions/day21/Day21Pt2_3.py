from dataclasses import dataclass
from enum import Enum

from solutions.solution import Solution
from utils.files import FileUtils

STEP_GOAL = 5000
# STEP_GOAL = 26501365

@dataclass
class ChunkPos:
    chunk_x: int
    chunk_y: int
    local_x: int
    local_y: int

    def __str__(self):
        return f"{self.chunk_x},{self.chunk_y}:{self.local_x},{self.local_y}"

    def key(self) -> str:
        return self.__str__()

    def above(self, grid: list[str]) -> "ChunkPos":
        if self.local_y <= 0:
            return ChunkPos(self.chunk_x, self.chunk_y-1, self.local_x, len(grid)-1)
        return ChunkPos(self.chunk_x, self.chunk_y, self.local_x, self.local_y-1)

    def below(self, grid: list[str]) -> "ChunkPos":
        if self.local_y >= len(grid)-1:
            return ChunkPos(self.chunk_x, self.chunk_y+1, self.local_x, 0)
        return ChunkPos(self.chunk_x, self.chunk_y, self.local_x, self.local_y+1)

    def left(self, grid: list[str]) -> "ChunkPos":
        if self.local_x <= 0:
            return ChunkPos(self.chunk_x-1, self.chunk_y, len(grid[0])-1, self.local_y)
        return ChunkPos(self.chunk_x, self.chunk_y, self.local_x-1, self.local_y)

    def right(self, grid: list[str]) -> "ChunkPos":
        if self.local_x >= len(grid[0])-1:
            return ChunkPos(self.chunk_x+1, self.chunk_y, 0, self.local_y)
        return ChunkPos(self.chunk_x, self.chunk_y, self.local_x+1, self.local_y)

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
    pos: ChunkPos
    polarity: Polarity
    step: int

class Day21Pt2_3Solution(Solution):
    grid: list[str]

    def run(self) -> None:
        self.grid = FileUtils.read_lines('resources/day21/test.txt')
        for line in self.grid:
            print(line)

        start = self._find_start()
        print(f"Start: {start}")
        print(f"Size: {len(self.grid[0])}x{len(self.grid)}")

        # Assign start '.' value so later comparisons are easier
        self.grid[start.local_y] = self.grid[start.local_y].replace('S', '.', 1)

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
            if self.grid[pos.local_y][pos.local_x] == '#': continue

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

            queue.append(QueueItem(pos.above(self.grid), next_polarity, next_step))
            queue.append(QueueItem(pos.below(self.grid), next_polarity, next_step))
            queue.append(QueueItem(pos.left(self.grid), next_polarity, next_step))
            queue.append(QueueItem(pos.right(self.grid), next_polarity, next_step))

        print(f"Num possibilities: {end_count}")


    def _find_start(self) -> ChunkPos:
        for y in range(0, len(self.grid)):
            row = self.grid[y]
            for x in range(0, len(row)):
                if row[x] == 'S':
                    return ChunkPos(0, 0, x, y)
        raise RuntimeError('Starting pos not found')