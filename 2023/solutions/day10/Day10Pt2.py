from enum import Enum
from solutions.solution import Solution
from utils.files import FileUtils

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
    grid: list[str]
    start: Pos2D

    def run(self) -> None:
        self.grid = FileUtils.read_lines('resources/day10/test4.txt')
        self.start = self.findStart()

        path: list[Pos2D] = []

        # Pick a start path
        pos, dir = self.pickFirstStep()
        path.append(pos)

        while self.valAtPos(pos) != 'S':
            pos, dir = self.nextStep(pos, dir)
            path.append(pos)


        # Create set of all positions which we intend to check to see if they are enclosed by the path or not.
        unchecked_positions = set()
        for y in range(0, len(self.grid)):
            for x in range(0, len(self.grid[y])):
                unchecked_positions.add(Pos2D(x, y))

        print(f"Unchecked positions: {unchecked_positions}")
        print(f"Path: {path}")
        for p in path:
            unchecked_positions.remove(p)

        # These will help with checks.
        path_set = set(path)
        enclosed_set = set()
        unenclosed_set = set()

        while len(unchecked_positions) > 0:
            pos = unchecked_positions.pop()
            enclosed, visited = self.checkEnclosed(pos, path_set)

            if enclosed:
                enclosed_set = enclosed_set.union(visited)
            else:
                unenclosed_set = unenclosed_set.union(visited)

            unchecked_positions = unchecked_positions.difference(visited)

        print("Enclosed:")
        for pos in enclosed_set:
            print(pos)
        print("\nUnenclosed:")
        for pos in unenclosed_set:
            print(pos)

        print(f"Num enclosed: {len(enclosed_set)}")
            

    def checkEnclosed(self, start: Pos2D, path_set: set[Pos2D]) -> tuple[bool, set[Pos2D]]:
        enclosed = True
        queue = [start]
        visited = set()

        while len(queue) > 0:
            pos = queue.pop()
            if pos.x < 0 or pos.x >= len(self.grid[0]) or pos.y < 0 or pos.y >= len(self.grid):
                enclosed = False
                continue
            if pos in visited:
                continue
            if pos in path_set:
                continue

            visited.add(pos)
            queue.append(pos.above())
            queue.append(pos.toRight())
            queue.append(pos.below())
            queue.append(pos.toLeft())

        return enclosed, visited


                

    def findStart(self) -> Pos2D:
        for y in range(0, len(self.grid)):
            for x in range(0, len(self.grid[y])):
                if self.grid[y][x] == 'S':
                    return Pos2D(x, y)
        raise ValueError("Starting position not found in grid")
    
    def pickFirstStep(self) -> tuple[Pos2D, Dir]:
        x = self.start.x
        y = self.start.y

        # If up valid, return.
        up = self.valAt(x, y-1)
        if up == '|' or up == 'F' or up == '7':
            return (Pos2D(x, y-1), Dir.U)
        
        # If right valid, return
        right = self.valAt(x+1, y)
        if right == '-' or right == '7' or right == 'J':
            return (Pos2D(x+1, y), Dir.R)
        
        # If down valid, return
        down = self.valAt(x, y+1)
        if down == '|' or down == 'L' or down == 'J':
            return (Pos2D(x, y+1), Dir.D)
        
        # Technically left need not be checked. At least one should have been found by rules of the input.
        raise 'Valid first step not found'
    
    def nextStep(self, pos: Pos2D, last_dir: Dir) -> tuple[Pos2D, Dir]:
        val = self.valAtPos(pos)

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
    
    def valAtPos(self, pos: Pos2D) -> str | None:
        return self.valAt(pos.x, pos.y)
    
    def valAt(self, x: int, y: int) -> str | None:
        if x < 0 or x >= len(self.grid[0]):
            return None
        if y < 0 or y >= len(self.grid):
            return None
        return self.grid[y][x]
    