package day08pt2

import (
	"fmt"

	"github.com/JacobMuchow/AdventOfCode/2024/utils"
)

type Grid = [][]rune

type Pos2d struct {
	x int
	y int
}

func Run() {
	lines := utils.ReadLinesFromFile("resources/day08_test.txt")

	grid := parseGrid(lines)

	freqMap := findFrequencies(grid)

	antinodes := make(map[string]bool, 0)

	// For all atennaes of a given frequency, look at all
	// combinations and determine the valid antinode positions.
	// Add the positions to a Set to keep track of the number of
	// unique positions.
	for _, points := range freqMap {
		for i := 0; i < len(points)-1; i++ {
			for j := i + 1; j < len(points); j++ {
				dx := points[j].x - points[i].x
				dy := points[j].y - points[i].y

				anPos := Pos2d{points[j].x + dx, points[j].y + dy}
				if posInGrid(anPos, grid) {
					antinodes[keyFor(anPos)] = true
				}

				anPos = Pos2d{points[i].x - dx, points[i].y - dy}
				if posInGrid(anPos, grid) {
					antinodes[keyFor(anPos)] = true
				}
			}
		}
	}

	fmt.Println("Num antinodes:", len(antinodes))
}

func findFrequencies(grid Grid) map[rune][]Pos2d {
	freqMap := make(map[rune][]Pos2d, 0)

	for y, row := range grid {
		for x, freq := range row {
			if row[x] == '.' {
				continue
			}
			freqMap[freq] = append(freqMap[freq], Pos2d{x, y})
		}
	}

	return freqMap
}

func parseGrid(lines []string) Grid {
	grid := make(Grid, len(lines))
	for y, line := range lines {
		grid[y] = []rune(line)
	}
	return grid
}

func keyFor(pos Pos2d) string {
	return fmt.Sprintf("%d,%d", pos.x, pos.y)
}

func posInGrid(pos Pos2d, grid Grid) bool {
	return pos.x >= 0 && pos.x < len(grid[0]) && pos.y >= 0 && pos.y < len(grid)
}
