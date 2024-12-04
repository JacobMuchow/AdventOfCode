package day04pt1

import (
	"fmt"

	"github.com/JacobMuchow/AdventOfCode/2024/utils"
)

type Grid = [][]rune

func Run() {
	lines := utils.ReadLinesFromFile("resources/day04_input.txt")

	grid := parseGrid(lines)

	wordCount := 0

	for y := range grid {
		for x := range grid[y] {
			wordCount += countWords(grid, x, y, []rune("XMAS"))
		}
	}

	fmt.Println("Total word count:", wordCount)
}

func countWords(grid Grid, x int, y int, word []rune) int {
	wordCount := 0

	wordCount += checkWordRecursive(grid, x, y, 1, 0, word, 0)   // Right
	wordCount += checkWordRecursive(grid, x, y, 1, 1, word, 0)   // Down-Right
	wordCount += checkWordRecursive(grid, x, y, 0, 1, word, 0)   // Down
	wordCount += checkWordRecursive(grid, x, y, -1, 1, word, 0)  // Down-Left
	wordCount += checkWordRecursive(grid, x, y, -1, 0, word, 0)  // Left
	wordCount += checkWordRecursive(grid, x, y, -1, -1, word, 0) // Up-Left
	wordCount += checkWordRecursive(grid, x, y, 0, -1, word, 0)  // Up
	wordCount += checkWordRecursive(grid, x, y, 1, -1, word, 0)  // Up-Right

	return wordCount
}

func checkWordRecursive(grid Grid, x int, y int, dx int, dy int, word []rune, idx int) int {
	// End of word reached, this works.
	if idx >= len(word) {
		return 1
	}

	// Gone out of bounds.
	if x < 0 || x >= len(grid[0]) || y < 0 || y >= len(grid) {
		return 0
	}

	// Character not a match.
	if grid[y][x] != word[idx] {
		return 0
	}

	// Check next
	return checkWordRecursive(grid, x+dx, y+dy, dx, dy, word, idx+1)
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
