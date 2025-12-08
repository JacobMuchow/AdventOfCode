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
    
    def __str__(self):
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

class Day10Pt1Solution(Solution):
    grid: list[str]
    start: Pos2D

    def run(self) -> None:
        self.grid = FileUtils.read_lines('resources/day10/input.txt')
        self.start = self.findStart()

        path: list[Pos2D] = []

        # Pick a start path
        pos, dir = self.pickFirstStep()
        path.append(pos)

        while self.valAtPos(pos) != 'S':
            pos, dir = self.nextStep(pos, dir)
            path.append(pos)

        halfway = int(len(path) / 2)
        print(f"Num steps: {halfway}")

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
    