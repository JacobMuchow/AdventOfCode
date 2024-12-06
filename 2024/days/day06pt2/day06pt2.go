package day06pt2

import (
	"fmt"

	"github.com/JacobMuchow/AdventOfCode/2024/utils"
)

type Grid = [][]rune

const (
	Up    = iota // 0
	Right        // 1
	Down         // 2
	Left         // 3
)

func Run() {
	lines := utils.ReadLinesFromFile("resources/day06_input.txt")

	grid := parseGrid(lines)
	for _, row := range grid {
		fmt.Println(string(row))
	}

	startX, startY := findStartPos(grid)
	fmt.Println("Start pos:", startX, startY)

	// Remove the marker for the guard from the grid.
	grid[startY][startX] = '.'

	possibleLoops := 0

	for y := range grid {
		for x := range grid {
			// Skip obstacles & starting position.
			if grid[y][x] == '#' || (x == startX && y == startY) {
				continue
			}

			// Place obstacle.
			grid[y][x] = '#'

			if detectLoop(grid, startX, startY) {
				possibleLoops += 1
			}

			// Remove obstacle.
			grid[y][x] = '.'
		}
	}

	fmt.Println("Potential loops:", possibleLoops)
}

func detectLoop(grid Grid, x int, y int) bool {
	// Will keep track of the visited places in a map, with a list of directions.
	visited := make(map[string]bool, 0)
	dir := Up

	for {
		key := posKey(x, y, dir)

		// Already visited this pos, facing this direction. This is a loop.
		if visited[key] {
			return true
		}
		visited[key] = true

		// Edge of grid, no way back.
		if x <= 0 || x >= len(grid[0])-1 || y <= 0 || y >= len(grid)-1 {
			return false
		}

		switch dir {
		case Up:
			if grid[y-1][x] == '.' {
				y -= 1
			} else {
				dir = Right
			}
		case Right:
			if grid[y][x+1] == '.' {
				x += 1
			} else {
				dir = Down
			}
		case Down:
			if grid[y+1][x] == '.' {
				y += 1
			} else {
				dir = Left
			}
		case Left:
			if grid[y][x-1] == '.' {
				x -= 1
			} else {
				dir = Up
			}
		}
	}
}

func findStartPos(grid Grid) (int, int) {
	for y, row := range grid {
		for x, char := range row {
			if char == '^' {
				return x, y
			}
		}
	}
	panic("Failed to find start pos")
}

func parseGrid(lines []string) Grid {
	grid := make(Grid, len(lines))

	for y, line := range lines {
		grid[y] = []rune(line)
	}

	return grid
}

func posKey(x int, y int, dir int) string {
	return fmt.Sprintf("%d,%d,%d", x, y, dir)
}
