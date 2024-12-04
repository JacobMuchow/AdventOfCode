package day04pt2

import (
	"fmt"

	"github.com/JacobMuchow/AdventOfCode/2024/utils"
)

type Grid = [][]rune

func Run() {
	lines := utils.ReadLinesFromFile("resources/day04_input.txt")

	grid := parseGrid(lines)

	xmasCount := 0

	for y := 1; y < len(grid)-1; y++ {
		for x := 1; x < len(grid[0])-1; x++ {
			if isXMAS(grid, y, x) {
				xmasCount += 1
			}
		}
	}

	fmt.Println("Total XMAS count:", xmasCount)
}

func isXMAS(grid Grid, x int, y int) bool {
	if grid[y][x] != 'A' {
		return false
	}

	tl := grid[y-1][x-1]
	tr := grid[y-1][x+1]
	br := grid[y+1][x+1]
	bl := grid[y+1][x-1]

	fwdLine := (tl == 'M' && br == 'S') || (tl == 'S' && br == 'M')
	bwdLine := (bl == 'M' && tr == 'S') || (bl == 'S' && tr == 'M')

	return fwdLine && bwdLine
}

func parseGrid(lines []string) Grid {
	grid := make(Grid, len(lines))

	for y, line := range lines {
		grid[y] = make([]rune, len(lines[y]))

		for x, char := range line {
			grid[y][x] = char
		}
	}

	return grid
}
