package day12pt1

import (
	"fmt"

	"github.com/JacobMuchow/AdventOfCode/2024/utils"
)

type Grid = [][]rune

type Pos2D struct {
	X int
	Y int
}

func Run() {
	lines := utils.ReadLinesFromFile("resources/day12_input.txt")
	grid := parseGrid(lines)
	printGrid(grid)

	regions := findRegions(grid)
	total := 0

	for _, region := range regions {
		price := fencePrice(grid, region)
		total += price
	}

	fmt.Printf("\nTotal: %d\n", total)
}

func parseGrid(lines []string) Grid {
	grid := make(Grid, len(lines))
	for y, line := range lines {
		grid[y] = []rune(line)
	}
	return grid
}

func findRegions(grid Grid) [][]Pos2D {
	// Add all positions to "unvisited" set.
	unvisited := make(map[Pos2D]bool, len(grid)*len(grid[0]))
	for y, row := range grid {
		for x := range row {
			unvisited[Pos2D{X: x, Y: y}] = true
		}
	}

	// Iterate on unvisited positions, draining the set until
	// all positions are visited and regions are collected.
	regions := make([][]Pos2D, 0)
	for {
		start, _, ok := popMap(unvisited)
		if !ok {
			break
		}

		region := []Pos2D{start}
		regionValue := grid[start.Y][start.X]
		queue := []Pos2D{above(start), right(start), below(start), left(start)}

		for {
			var pos Pos2D
			pos, queue, ok = popFirst(queue)
			if !ok {
				break
			}

			if pos.Y < 0 || pos.Y >= len(grid) || pos.X < 0 || pos.X >= len(grid[0]) {
				continue
			}

			if grid[pos.Y][pos.X] != regionValue {
				continue
			}

			_, exists := unvisited[pos]
			if !exists {
				continue
			}
			delete(unvisited, pos)
			region = append(region, pos)
			queue = append(queue, above(pos), right(pos), below(pos), left(pos))
		}

		regions = append(regions, region)
	}

	return regions
}

func fencePrice(grid Grid, region []Pos2D) int {
	area := len(region)
	perim := perimiter(grid, region)
	return area * perim
}

func perimiter(grid Grid, region []Pos2D) int {
	// We can consider each position to have 4 fences lines on its permiter.
	// Then subtract N neighbors for each position.
	perim := 4 * len(region)
	regionVal := grid[region[0].Y][region[0].X]

	for _, pos := range region {
		if pos.Y > 0 && grid[pos.Y-1][pos.X] == regionVal {
			perim -= 1
		}
		if pos.Y < len(grid)-1 && grid[pos.Y+1][pos.X] == regionVal {
			perim -= 1
		}
		if pos.X > 0 && grid[pos.Y][pos.X-1] == regionVal {
			perim -= 1
		}
		if pos.X < len(grid[0])-1 && grid[pos.Y][pos.X+1] == regionVal {
			perim -= 1
		}
	}

	return perim
}

func printGrid(grid Grid) {
	for _, row := range grid {
		println(string(row))
	}
}

func posKey(x int, y int) string {
	return fmt.Sprintf("%d,%d", x, y)
}

func popMap[K comparable, V any](m map[K]V) (K, V, bool) {
	for key, value := range m {
		delete(m, key)
		return key, value, true
	}

	var zeroK K
	var zeroV V
	return zeroK, zeroV, false
}

func popFirst[T any](s []T) (T, []T, bool) {
	if len(s) > 0 {
		item := s[0]
		s = s[1:]
		return item, s, true
	}

	var zeroT T
	var zeroS []T
	return zeroT, zeroS, false
}

func above(pos Pos2D) Pos2D {
	return Pos2D{pos.X, pos.Y - 1}
}
func below(pos Pos2D) Pos2D {
	return Pos2D{pos.X, pos.Y + 1}
}
func left(pos Pos2D) Pos2D {
	return Pos2D{pos.X - 1, pos.Y}
}
func right(pos Pos2D) Pos2D {
	return Pos2D{pos.X + 1, pos.Y}
}
