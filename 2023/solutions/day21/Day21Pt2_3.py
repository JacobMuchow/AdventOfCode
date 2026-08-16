from dataclasses import dataclass
from enum import Enum
from math import floor

from solutions.solution import Solution
from utils.files import FileUtils

# STEP_GOAL = 26501365
STEP_GOAL = 115

@dataclass
class Pos2D:
    x: int
    y: int

    def __str__(self):
        return self.key()

    def key(self) -> str:
        return f"{self.x},{self.y}"

    def above(self) -> "Pos2D":
        return Pos2D(self.x, self.y-1)
    def below(self) -> "Pos2D":
        return Pos2D(self.x, self.y+1)
    def left(self) -> "Pos2D":
        return Pos2D(self.x-1, self.y)
    def right(self) -> "Pos2D":
        return Pos2D(self.x+1, self.y)

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

class Day21Pt2_3Solution(Solution):
    grid: list[str]
    grid_size: int
    start: Pos2D

    def run(self) -> None:
        self.grid = FileUtils.read_lines('resources/day21/test2.txt')
        self.grid_size = len(self.grid)
        grid_radius = floor(self.grid_size/2)
        grid_steps = (STEP_GOAL - grid_radius) / self.grid_size
        goal_polarity = Polarity.of(STEP_GOAL)

        start = self._find_start()
        # Assign start '.' value so later comparisons are easier
        self.grid[start.y] = self.grid[start.y].replace('S', '.', 1)

        for line in self.grid:
            print(line)
        print(f"Grid Size: {self.grid_size}x{self.grid_size}")
        print(f"Grid Radius: {grid_radius}")
        print(f"Grid Steps: {grid_steps}")
        print(f"Start: {start}")

        # Check grid is square
        if len(self.grid) != len(self.grid[0]):
            raise ValueError("Grid is not square")

        # Validate start is in middle
        if start.x != start.y or start.x != floor(self.grid_size/2):
            raise ValueError("Start pos not in center")

        # Check total grid steps is whole
        if grid_steps != floor(grid_steps):
            raise ValueError("Grid steps expected to be whole")

        # Odd whole tiles = (grid_steps-1)^2
        # Even whole tiles = (grid_steps)^2
        # 0,0 Large corners = N-1
        # 0,0 Small corners = N
        # ... repeat for grid_size,0
        # ... repeat for grid_size,grid_size
        # ... repeat for 0,grid_size
        # 1 Triangle grid_size/2,grid_size
        # 1 Triangle grid_size/2,0
        # 1 Triangle 0,grid_size/2
        # 1 Triangle grid_size,grid_size/2

        # Large corner step budget = STEP_GOAL - ((grid_size-1) + (grid_steps-2)*(4*grid_radius)
        # Small corner step budget = STEP_GOAL - (2*grid_radius + (grid_steps-1)*(4*grid_radius))

        # Compute values of different tile types
        even_tile_value = self._count_end_spots(start, Polarity.Even, goal_polarity, step_limit=None, debug_label="Even Tile")
        odd_tile_value = self._count_end_spots(start, Polarity.Odd, goal_polarity, step_limit=None, debug_label="Odd Tile")

        axial_corner_steps_left = self.grid_size-1
        large_corner_steps_left = STEP_GOAL - (2*grid_radius + (grid_steps-2)*self.grid_size)
        small_corner_steps_left = STEP_GOAL - (2*grid_radius + (grid_steps-1)*self.grid_size)

        n_corner_value = self._count_end_spots(Pos2D(grid_radius,      self.grid_size-1), goal_polarity, goal_polarity, axial_corner_steps_left, debug_label="North Corner")
        s_corner_value = self._count_end_spots(Pos2D(grid_radius,      0),                goal_polarity, goal_polarity, axial_corner_steps_left, debug_label="South Corner")
        e_corner_value = self._count_end_spots(Pos2D(0,                grid_radius),      goal_polarity, goal_polarity, axial_corner_steps_left, debug_label="East Corner")
        w_corner_value = self._count_end_spots(Pos2D(self.grid_size-1, grid_radius),      goal_polarity, goal_polarity, axial_corner_steps_left, debug_label="West Corner")

        val_odd_whole_tiles = pow(grid_steps-1, 2) * odd_tile_value
        val_even_whole_tiles = pow(grid_steps, 2) * even_tile_value

        total = val_odd_whole_tiles \
            + val_even_whole_tiles

        return

    def _count_end_spots(self, 
        start: Pos2D, 
        start_polarity: Polarity, 
        goal_polarity: Polarity,
        step_limit: int | None,
        debug_label: str
    ) -> int:
        # Set up optimized search queue
        queue: list[QueueItem] = [QueueItem(start, start_polarity, step=0)]
        seen: set[str] = set()
        end_count = 0
        goal_polarity = Polarity.of(STEP_GOAL)

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
            if step_limit and item.step >= step_limit:
                continue

            # Enqueue future step possibilities. 
            # Guard on popping the item covers out-of-bounds and invalid tiles.
            next_polarity = item.polarity.flip()
            next_step = item.step + 1

            queue.append(QueueItem(pos.above(), next_polarity, next_step))
            queue.append(QueueItem(pos.below(), next_polarity, next_step))
            queue.append(QueueItem(pos.right(), next_polarity, next_step))
            queue.append(QueueItem(pos.left(), next_polarity, next_step))

        # print grid showing 
        print(f"\n\n{debug_label}:")
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                if Pos2D(x, y).key() in seen:
                    print('*', end="")
                else:
                    print(self.grid[y][x], end="")
            print("")

        return end_count

    def _find_start(self) -> Pos2D:
        for y in range(0, len(self.grid)):
            row = self.grid[y]
            for x in range(0, len(row)):
                if row[x] == 'S':
                    return Pos2D(x, y)
        raise RuntimeError('Starting pos not found')