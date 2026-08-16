from dataclasses import dataclass
from enum import Enum
from math import floor

from solutions.solution import Solution
from utils.files import FileUtils

STEP_GOAL = 26501365
# STEP_GOAL = 115

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
        """
        My first attempts involved a BFS approach but storing a "chunked" coorindate, so you would index back into the same
        map instead of duplicating memory. I knew based on the question this wasn't going to be enough because the new step
        goal was incredibly high. Where I messed up is thinking this grid-memory solution mattered. I thought it was a first
        step in a potential cached computation approach and I would figure out the rest when I got there. But this is a bad
        path. It couldn't even solve the 5000 step example on an 11x11 grid in a reasonable time.

        Note: when I refer to "value", it is the number of reachable endpoints in the given chunk/tile.

        Early on, I noticed 4 things: 
        1. The edge around both the test & input grids is completely empty.
        2. The start is always in the middle.
        3. In the input specificaly, column and row cutting across the mid-point are both empty.
        4. There will be 2 types of filled tyles. Ones with "Even" polarity and ones with "Odd", because the grid size is odd.

        I figured these are crucial to the problem and that is right. There are some interesting emergent properties.
        - You can always travel in cardinal directions unimpeded. 
            - This means the "shape" grows to be the exact step count in all cardinal directions.
        - You can also travel in manhattan diagonals unimpeded.
            - This means the diagonal growth of the shape is consistent.
            - As a matter of fact, it produces roughly a square diamond shape.

        So I pictured a solution where you count all the whole Even/Odd tiles stored inside the shape, compute once
        the value of each and multiply the counts, and this gets you *pretty* close to the solution. But what I wasn't
        sure about was the edges of this shape. Eventualy I succumbed and looked up help :) A lot of folks solved this 
        quadratically - which makes sense now that I fully absorbed the problem - but my mind was more interested in the 
        geometric solutions.

        That's where this post came up huge: 
        https://github.com/villuna/aoc23/wiki/A-Geometric-solution-to-advent-of-code-2023,-day-21

        I unlocked 2 critical breakthroughs:
        1. The step goal is derived cleanly from the input grid size. It is simply the dist to escape the first chunk (65) +
            a multiple N ("grid_steps") * grid_size. In other words, once you subtract 65 to becomes cleanly divisible.
        2. The diamon shape isn't just _rough_ it's exactly a diamond due to the unimpeded travel on diagonal, horizontal 
            and vertical axis.

        After understanding this, the pieces started to fit more into place. But I wanted to take a slightly different approach 
        from the blog post. 

        Interesting emergent properties of the input are:
        - The shortest path to reach any tile type (and thus - most steps left) always arrives at the same point per tile type,
            regardless of position. This is due to the unimpeded manhattan travel + diamond shape. Ex) For any of the corners 
            facing NE, the shortest path to enter this chunk always brings you to 0,130 on entering the chunk, and always with
            X steps remaining.
        - This means each "NE large corner" has the same vlue, regardless of position.
        - The number of whole Odd tiles, whole Even tiles, large corners and small corners are all derivable from the number N -
            number of whole grids traversed walking in one cardinal direction.

        So the solution that took shape in my mind was to calculate the values of each of these types + the number of appearances,
        add it all up and you've got your answer, which hopefully you can follow below.
        """
        self.grid = FileUtils.read_lines('resources/day21/input.txt')
        self.grid_size = len(self.grid)

        grid_radius = floor(self.grid_size/2) # 65
        grid_steps = (STEP_GOAL - grid_radius) / self.grid_size # Big numero
        goal_polarity = Polarity.of(STEP_GOAL) # odd

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

        ####### Calculate how many steps will be left for each type of corner piece of the shapes edge.
        # 131 before entering, but 130 after.
        nesw_corner_steps_left = self.grid_size-1 
        # steps to reach corner of first chunk + steps to arrive to corner just outside of our target + 2 more steps to step inside.
        large_corner_steps_left = STEP_GOAL - (2*grid_radius + (grid_steps-2)*self.grid_size + 2) 
        small_corner_steps_left = STEP_GOAL - (2*grid_radius + (grid_steps-1)*self.grid_size + 2)

        print(f"NESW corner steps: {nesw_corner_steps_left}")
        print(f"Large corner steps: {large_corner_steps_left}")
        print(f"Small corner steps: {small_corner_steps_left}")

        ###### Compute values of different tile types
        # Why is odd .Even and even .Odd? -> Just a quirk of how you think about it. The very first chunk: you start Even, but the goal is Odd.
        odd_tile_value = self._count_end_spots(start, Polarity.Even, goal_polarity, step_limit=None, debug_label="Odd Tile")
        even_tile_value = self._count_end_spots(start, Polarity.Odd, goal_polarity, step_limit=None, debug_label="Even Tile")

        # For each of these, we need to know (1) start point (easy since it's manhattan); (2) polarity of that point (think carefully); (3) steps left (calculated above)
        n_corner_value = self._count_end_spots(Pos2D(grid_radius,      self.grid_size-1), Polarity.Odd, goal_polarity, nesw_corner_steps_left, debug_label="North Corner")
        e_corner_value = self._count_end_spots(Pos2D(0,                grid_radius),      Polarity.Odd, goal_polarity, nesw_corner_steps_left, debug_label="East Corner")
        s_corner_value = self._count_end_spots(Pos2D(grid_radius,      0),                Polarity.Odd, goal_polarity, nesw_corner_steps_left, debug_label="South Corner")
        w_corner_value = self._count_end_spots(Pos2D(self.grid_size-1, grid_radius),      Polarity.Odd, goal_polarity, nesw_corner_steps_left, debug_label="West Corner")

        ne_sm_corner_val = self._count_end_spots(Pos2D(0,                self.grid_size-1), Polarity.Odd, goal_polarity, small_corner_steps_left, debug_label="NE Small Corner")
        ne_lg_corner_val = self._count_end_spots(Pos2D(0,                self.grid_size-1), Polarity.Even,  goal_polarity, large_corner_steps_left, debug_label="NE Large Corner")
        se_sm_corner_val = self._count_end_spots(Pos2D(0,                0),                Polarity.Odd, goal_polarity, small_corner_steps_left, debug_label="SE Small Corner")
        se_lg_corner_val = self._count_end_spots(Pos2D(0,                0),                Polarity.Even,  goal_polarity, large_corner_steps_left, debug_label="SE Large Corner") 
        sw_sm_corner_val = self._count_end_spots(Pos2D(self.grid_size-1, 0),                Polarity.Odd, goal_polarity, small_corner_steps_left, debug_label="SW Small Corner")        
        sw_lg_corner_val = self._count_end_spots(Pos2D(self.grid_size-1, 0),                Polarity.Even,  goal_polarity, large_corner_steps_left, debug_label="SW Large Corner")
        nw_sm_corner_val = self._count_end_spots(Pos2D(self.grid_size-1, self.grid_size-1), Polarity.Odd, goal_polarity, small_corner_steps_left, debug_label="NW Small Corner")
        nw_lg_corner_val = self._count_end_spots(Pos2D(self.grid_size-1, self.grid_size-1), Polarity.Even,  goal_polarity, large_corner_steps_left, debug_label="NW Large Corner")

        # Now calculate the total value per each type (num tiles * value per tile)
        val_odd_whole_tiles = pow(grid_steps-1, 2) * odd_tile_value
        val_even_whole_tiles = pow(grid_steps, 2) * even_tile_value
        val_ne_lg_corners = (grid_steps-1) * ne_lg_corner_val
        val_ne_sm_corners = grid_steps * ne_sm_corner_val
        val_se_lg_corners = (grid_steps-1) * se_lg_corner_val
        val_se_sm_corners = grid_steps * se_sm_corner_val
        val_sw_lg_corners = (grid_steps-1) * sw_lg_corner_val
        val_sw_sm_corners = grid_steps * sw_sm_corner_val
        val_nw_lg_corners = (grid_steps-1) * nw_lg_corner_val
        val_nw_sm_corners = grid_steps * nw_sm_corner_val

        # Now sum it all up
        total = floor(val_odd_whole_tiles \
            + val_even_whole_tiles \
            + n_corner_value \
            + e_corner_value \
            + s_corner_value \
            + w_corner_value \
            + val_ne_lg_corners \
            + val_ne_sm_corners \
            + val_se_lg_corners \
            + val_se_sm_corners \
            + val_sw_lg_corners \
            + val_sw_sm_corners \
            + val_nw_lg_corners \
            + val_nw_sm_corners)

        print(f"Total: {total}")
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
        # print(f"\n\n{debug_label}:")
        # for y in range(self.grid_size):
        #     for x in range(self.grid_size):
        #         if Pos2D(x, y).key() in seen:
        #             print('*', end="")
        #         else:
        #             print(self.grid[y][x], end="")
        #     print("")

        return end_count

    def _find_start(self) -> Pos2D:
        for y in range(0, len(self.grid)):
            row = self.grid[y]
            for x in range(0, len(row)):
                if row[x] == 'S':
                    return Pos2D(x, y)
        raise RuntimeError('Starting pos not found')