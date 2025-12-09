from enum import Enum
from solutions.solution import Solution
from utils.files import FileUtils

type Grid = list[list[str]]

class Dir(Enum):
    R = 'R'
    L = 'L'
    U = 'U'
    D = 'D'

class Pos2D:
    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def key(self) -> str:
        return f"{self.x},{self.y}"
    
    def __hash__(self):
        return self.key().__hash__()
    
    def __eq__(self, other):
        if not isinstance(other, Pos2D):
            return False
        return self.x == other.x and self.y == other.y
    
    def __str__(self):
        return self.key()
    
    def __repr__(self):
        return self.key()
    
    def neighbor(self, dir: Dir) -> "Pos2D":
        if dir == Dir.R:
            return self.toRight()
        if dir == Dir.L:
            return self.toLeft()
        if dir == Dir.U:
            return self.above()
        if dir == Dir.D:
            return self.below()
    def toRight(self):
        return Pos2D(self.x+1, self.y)
    def toLeft(self):
        return Pos2D(self.x-1, self.y)
    def above(self):
        return Pos2D(self.x, self.y-1)
    def below(self):
        return Pos2D(self.x, self.y+1)

class Day10Pt2Solution(Solution):
    def run(self) -> None:
        lines = FileUtils.read_lines('resources/day10/input.txt')
        grid = [list(line) for line in lines]
        start = self.findStart(grid)

        path = self.findPath(grid, start)
        path_set = set(path)

        # Create set of all positions which we intend to check to see if they are enclosed by the path or not.
        # Also remove all the extra pipes not in the path.
        unchecked_positions = set()
        for y in range(0, len(grid)):
            for x in range(0, len(grid[y])):
                pos = Pos2D(x, y)
                if pos not in path_set:
                    grid[y][x] = '.'
                    unchecked_positions.add(pos)

        # Now final all potential enclosed positions in the grid.
        enclosed_set: set[Pos2D] = set()

        while len(unchecked_positions) > 0:
            pos = unchecked_positions.pop()
            enclosed, visited = self.checkEnclosed(grid, pos)

            if enclosed:
                enclosed_set = enclosed_set.union(visited)

            unchecked_positions = unchecked_positions.difference(visited)

        print(f"# Candidate Enclosed: {len(enclosed_set)}")

        # Now expand the grid, then veryify if all the enclosed positions are still enclosed.
        expanded_grid = self.expandGrid(grid, path)
        
        final_enclosed_set: set[Pos2D] = set(enclosed_set)
        while len(enclosed_set) > 0:
            pos = enclosed_set.pop()
            enclosed, visited = self.checkEnclosed(expanded_grid, Pos2D(pos.x*2, pos.y*2))

            visited = set([Pos2D(int(p.x/2), int(p.y/2)) for p in visited if p.x % 2 == 0 and p.y % 2 == 0])

            if not enclosed:
                final_enclosed_set = final_enclosed_set.difference(visited)
            enclosed_set = enclosed_set.difference(visited)
        
        print(f"# Final Enclosed: {len(final_enclosed_set)}")
        

    def printGrid(self, grid: Grid):
        for row in grid:
            print(''.join(row))

    def findPath(self, grid: Grid, start: Pos2D) -> list[Pos2D]:
        path: list[Pos2D] = []

        # Pick a start path
        pos, dir = self.pickFirstStep(grid, start)
        path.append(pos)

        print(f"POS: {pos}")

        while self.valAtPos(grid, pos) != 'S':
            pos, dir = self.nextStep(grid, pos, dir)
            path.append(pos)

        return path
            
    def expandGrid(self, grid: Grid, path: list[Pos2D]) -> list[str]:
        new_h = len(grid) * 2
        new_w = len(grid[0]) * 2
        new_grid = [['.' for _ in range(new_w)] for _ in range(0, new_h)]
        path_set = set(path)
                
        for y in range(0, new_h, 2):
            for x in range(0, new_w, 2):
                pos = Pos2D(int(x/2), int(y/2))
                if pos not in path_set:
                    new_grid[y][x] = '.'
                    new_grid[y][x+1] = '.'
                    new_grid[y+1][x] = '.'
                    new_grid[y+1][x+1] = '.'
                else:
                    val = self.valAtPos(grid, pos)
                    if val == 'S':
                        val = self.pipeTypeOfStart(path)

                    new_grid[y][x] = val
                    if val == '-' or val == 'F' or val == 'L':
                        new_grid[y][x+1] = '-'
                    else:
                        new_grid[y][x+1] = '.'
                    if val == '|' or val == 'F' or val == '7':
                        new_grid[y+1][x] = '|'
                    else:
                        new_grid[y+1][x] = '.'
                    new_grid[y+1][x+1] = '.'

        return [''.join(row) for row in new_grid]
                
    def pipeTypeOfStart(self, path: list[Pos2D]) -> str:
        first = path[0]
        last = path[len(path)-2]
        dx = last.x - first.x
        dy = last.y - first.y

        if dx == 0 and abs(dy) == 2:
            return '|'
        if dy == 0 and abs(dx) == 2:
            return '-'
        if dx == 1 and dy == 1:
            return '7'
        if dx == 1 and dy == -1:
            return 'J'
        if dx == -1 and dy == 1:
            return 'F'
        if dx == -1 and dy == -1:
            return 'L'
        
        raise Exception('Error figuring out pipe type for start')
            
    def checkEnclosed(self, grid: Grid, start: Pos2D) -> tuple[bool, set[Pos2D]]:
        enclosed = True
        queue = [start]
        visited = set()

        while len(queue) > 0:
            pos = queue.pop()
            if pos.x < 0 or pos.x >= len(grid[0]) or pos.y < 0 or pos.y >= len(grid):
                enclosed = False
                continue
            if pos in visited:
                continue
            if self.valAtPos(grid, pos) != '.':
                continue

            visited.add(pos)
            queue.append(pos.above())
            queue.append(pos.toRight())
            queue.append(pos.below())
            queue.append(pos.toLeft())

        return enclosed, visited     

    def findStart(self, grid: Grid) -> Pos2D:
        for y in range(0, len(grid)):
            for x in range(0, len(grid[y])):
                if grid[y][x] == 'S':
                    return Pos2D(x, y)
        raise ValueError("Starting position not found in grid")
    
    def pickFirstStep(self, grid: Grid, start: Pos2D) -> tuple[Pos2D, Dir]:
        # If up valid, return.
        up = self.valAtPos(grid, start.above())
        if up == '|' or up == 'F' or up == '7':
            return (start.above(), Dir.U)
        
        # If right valid, return
        right = self.valAtPos(grid, start.toRight())
        if right == '-' or right == '7' or right == 'J':
            return (start.toRight(), Dir.R)
        
        # If down valid, return
        down = self.valAtPos(grid, start.below())
        if down == '|' or down == 'L' or down == 'J':
            return (start.below(), Dir.D)
        
        # Technically left need not be checked. At least one should have been found by rules of the input.
        raise 'Valid first step not found'
    
    def nextStep(self, grid: Grid, pos: Pos2D, last_dir: Dir) -> tuple[Pos2D, Dir]:
        val = self.valAtPos(grid, pos)

        if val == '-':
            if last_dir == Dir.R:
                return [pos.toRight(), Dir.R]
            if last_dir == Dir.L:
                return [pos.toLeft(), Dir.L]
        elif val == '|':
            if last_dir == Dir.U:
                return [pos.above(), Dir.U]
            if last_dir == Dir.D:
                return [pos.below(), Dir.D]
        elif val == 'J':
            if last_dir == Dir.R:
                return [pos.above(), Dir.U]
            if last_dir == Dir.D:
                return [pos.toLeft(), Dir.L]
        elif val == '7':
            if last_dir == Dir.R:
                return [pos.below(), Dir.D]
            if last_dir == Dir.U:
                return [pos.toLeft(), Dir.L]
        elif val == 'L':
            if last_dir == Dir.L:
                return [pos.above(), Dir.U]
            if last_dir == Dir.D:
                return [pos.toRight(), Dir.R]
        elif val == 'F':
            if last_dir == Dir.L:
                return [pos.below(), Dir.D]
            if last_dir == Dir.U:
                return [pos.toRight(), Dir.R]
              
        raise Exception(f'Unepxected situation pos: {pos}, val: {val}, last_dir: {last_dir}')
    
    def valAtPos(self, grid: Grid, pos: Pos2D) -> str | None:
        return self.valAt(grid, pos.x, pos.y)
    
    def valAt(self, grid: Grid, x: int, y: int) -> str | None:
        if x < 0 or x >= len(grid[0]):
            return None
        if y < 0 or y >= len(grid):
            return None
        return grid[y][x]
    