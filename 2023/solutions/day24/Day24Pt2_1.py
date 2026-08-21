from dataclasses import dataclass
from fractions import Fraction

from solutions.solution import Solution
from utils.files import FileUtils

@dataclass
class Vector:
    x: Fraction
    y: Fraction
    z: Fraction

    def __str__(self):
        return f"({self.x},{self.y},{self.z})"
    

@dataclass
class Object:
    p: Vector
    v: Vector

    def __str__(self):
        return f"Pos={self.p}, Vel={self.v}"

class Day24Pt2_1Solution(Solution):

    def run(self) -> None:
        lines = FileUtils.read_lines('resources/day24/input.txt')

        # Only the first 3 stones are needed to compute the answer.
        stone1 = self.parse_stone(lines[0])
        stone2 = self.parse_stone(lines[1])
        stone3 = self.parse_stone(lines[2])
        print(F"Stone: {stone1}")
        print(F"Stone: {stone2}")
        print(F"Stone: {stone3}")

        # For each pair of stones we can create 3 distinct linear equations.
        # There are 6 unknowns (Rock's pos/vel: Px, Py, Pz, Vx, Vy, Vz).
        # This means we only need 6 total linear equations to create a solvable system.
        eqs12 = self.equations_for_pair(stone1, stone2)
        eqs13 = self.equations_for_pair(stone1, stone3)
        mat = eqs12 + eqs13

        soln = self.guassian_solve(mat)
        total = soln[0].numerator + soln[1].numerator + soln[2].numerator

        print(f"Total: {total}")

    def parse_stone(self, line: str) -> Object:
        tokens = line.split("@")
        pos_tokens = list(map(Fraction, tokens[0].split(",")))
        vel_tokens = list(map(Fraction, tokens[1].split(",")))

        return Object(
            Vector(pos_tokens[0], pos_tokens[1], pos_tokens[2]),
            Vector(vel_tokens[0], vel_tokens[1], vel_tokens[2])
        )

    def equations_for_pair(self, si: Object, sj: Object) -> list[Fraction]:
        # Deltas - compute once.
        dpx = si.p.x - sj.p.x
        dpy = si.p.y - sj.p.y
        dpz = si.p.z - sj.p.z
        dvx = si.v.x - sj.v.x
        dvy = si.v.y - sj.v.y
        dvz = si.v.z - sj.v.z

        # These were derived by hand using some matrix math.
        rowX = [   0,  dvz, -dvy,    0, -dpz,  dpy]
        rowY = [-dvz,    0,  dvx,  dpz,    0, -dpx]
        rowZ = [ dvy, -dvx,    0, -dpy,  dpx,    0]

        # Right hands. We'll just append to the results.
        rowX.append(si.p.y*si.v.z - si.p.z*si.v.y - sj.p.y*sj.v.z + sj.p.z*sj.v.y)
        rowY.append(si.p.z*si.v.x - si.p.x*si.v.z - sj.p.z*sj.v.x + sj.p.x*sj.v.z)
        rowZ.append(si.p.x*si.v.y - si.p.y*si.v.x - sj.p.x*sj.v.y + sj.p.y*sj.v.x)

        return [rowX, rowY, rowZ]

    def guassian_solve(self, mat: list[list[Fraction]]) -> list[Fraction]:
        """
        Returns an array, one value for each computed coefficient to the solution.
        These correspond to Px, Py, Pz, Vx, Vy, Vz.
        """

        def find_target_row(col: int, start_row: int) -> int:
            "Given a target column & starting row, search downward (inclusive) to find"
            "the next valid row. Valid means the value at rowxcol != 0."
            row = start_row
            while row < len(mat):
                if mat[row][col] != 0:
                    return row
                row += 1
            raise RuntimeError('No valid target row found')

        # Guassian solution involves an iteration over each column LTR.
        # 1. For reach column, we check the rows top-to-bottom to pick a pivot
        #   row to float to the top. 
        # 2. The remaining rows beneath get the value in that column zeroed out.
        #   This is done by multiplying by the factor of the coefficients. The entire
        #   row's values are subtracted by the associated pivot row value.
        col = 0
        while col < len(mat):
            pivot = find_target_row(col, start_row=col)

            # Move pivot up.
            if pivot != col:
                pivot_row = mat.pop(pivot)
                mat.insert(col, pivot_row)
                pivot = col
            
            # For each row below, if the value in the col is not zero we need to zero it out.
            # We compute factor for the key coefficient, then for each coefficient in the row,
            # subtract corresponding pivot value * factor. At the end, we can unwind the whole
            # thing to compute all the unknown values.
            for j in range(pivot+1, len(mat)):
                if mat[j][col] == 0: continue
                factor = mat[j][col] / mat[pivot][col]
                for i in range(0, len(mat[0])):
                    mat[j][i] = mat[j][i] - (factor * mat[pivot][i])

            col += 1

        # Compute final solutions
        row = len(mat) - 1
        rhi = len(mat[0]) - 1
        soln = [0] * len(mat)

        while row >= 0:
            ans = mat[row][rhi]

            col = row+1
            while col < rhi:
                ans -= mat[row][col] * soln[col]
                col += 1
            ans /= mat[row][row]

            soln[row] = ans
            row -= 1

        return soln


