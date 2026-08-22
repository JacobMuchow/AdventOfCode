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
	lines := utils.ReadLinesFromFile("resources/day12_test3.txt")
	grid := parseGrid(lines)
	printGrid(grid)

	regions := findRegions(grid)

	for _, region := range regions {
		regionVal := grid[region[0].Y][region[0].X]
		fmt.Printf("%c: %d\n", regionVal, len(region))
	}
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
