package day06pt1

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

	x, y := findStartPos(grid)
	fmt.Println("Start pos:", x, y)

	// Remove the marker for the guard from the grid.
	grid[y][x] = '.'
	dir := Up

	// Will keep track of the visited places in a map.
	visited := make(map[string]bool, 0)
	visited[posKey(x, y)] = true

	for {
		visited[posKey(x, y)] = true

		// Edge of grid, no way back.
		if x <= 0 || x >= len(grid[0])-1 || y <= 0 || y >= len(grid)-1 {
			break
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

	fmt.Println("Total visited:", len(visited))
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

func posKey(x int, y int) string {
	return fmt.Sprintf("%d,%d", x, y)
}
