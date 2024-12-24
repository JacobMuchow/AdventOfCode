package day10pt1

import (
	"fmt"

	"github.com/JacobMuchow/AdventOfCode/2024/utils"
)

type Grid = [][]int

func Run() {
	lines := utils.ReadLinesFromFile("resources/day10_test.txt")

	grid := parseGrid(lines)
	printGrid(grid)
}

func parseGrid(lines []string) *Grid {
	grid := make(Grid, len(lines))

	for y, line := range lines {
		row := make([]int, len(line))
		for x, char := range line {
			if char == '.' {
				row[x] = -1
			} else {
				row[x] = utils.ParseInt(string(char))
			}
		}
		grid[y] = row
	}

	return &grid
}

func printGrid(grid *Grid) {
	for _, row := range *grid {
		for _, val := range row {
			if val == -1 {
				fmt.Printf(".")
			} else {
				fmt.Printf("%d", val)
			}
		}
		fmt.Println()
	}
}
