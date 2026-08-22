package day12pt2

import (
	"cmp"
	"fmt"
	"slices"

	"github.com/JacobMuchow/AdventOfCode/2024/utils"
)

type Grid = [][]rune

type Pos2D struct {
	X int
	Y int
}

type Direction int

const (
	North Direction = iota
	East
	South
	West
)

func (d Direction) String() string {
	switch d {
	case North:
		return "North"
	case East:
		return "East"
	case South:
		return "South"
	case West:
		return "West"
	default:
		panic("Invalid direction")
	}
}

type Border struct {
	P1  Pos2D
	P2  Pos2D
	Dir Direction
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
	sides := countSides(grid, region)
	return area * sides
}

func countSides(grid Grid, region []Pos2D) int {
	regionVal := grid[region[0].Y][region[0].X]

	// Create a list of all "Border" relationships. This is a given tile
	// pos + a direction (side). Created by checking if the neighbor in
	// this dir is a different value.
	borders := make([]Border, 0)

	for _, pos := range region {
		if pos.Y <= 0 || grid[pos.Y-1][pos.X] != regionVal {
			borders = append(borders, Border{pos, pos, North})
		}
		if pos.Y >= len(grid)-1 || grid[pos.Y+1][pos.X] != regionVal {
			borders = append(borders, Border{pos, pos, South})
		}
		if pos.X <= 0 || grid[pos.Y][pos.X-1] != regionVal {
			borders = append(borders, Border{pos, pos, West})
		}
		if pos.X >= len(grid[0])-1 || grid[pos.Y][pos.X+1] != regionVal {
			borders = append(borders, Border{pos, pos, East})
		}
	}

	// Now we have to link distinct segments. We will iterate over all borders
	// combining distinct segments into longer pieces. We begin by sorting by
	// direction of the border for more efficient iteration.
	slices.SortFunc(borders, func(a Border, b Border) int {
		return cmp.Compare(a.Dir, b.Dir)
	})

	// Double-pointer iteration. Checking each border piece for any possible connections
	// and merging them. The pivot border is updated in place, and the other border is
	// removed from the list.
	i := 0
	for {
		if i >= len(borders) {
			break
		}

		j := i + 1
		bi := borders[i]

		for {
			if j >= len(borders) {
				break
			}
			bj := borders[j]
			if bj.Dir != bi.Dir {
				break
			}
			bf, fused := fuseIfConnected(bi, bj)
			if fused {
				// bf replaces bi; remove bj; reset j to i+1 and search again.
				bi = bf
				borders[i] = bi
				borders = slices.Delete(borders, j, j+1)
				j = i + 1
			} else {
				j += 1
			}
		}

		i += 1
	}

	return len(borders)
}

func fuseIfConnected(b1 Border, b2 Border) (Border, bool) {
	var zeroB Border

	// Must be same dir
	if b1.Dir != b2.Dir {
		return zeroB, false
	}

	// Checks for N/S and likewise E/W are the same.
	if b1.Dir == North || b1.Dir == South {
		// Y's must match.
		if b1.P1.Y == b2.P1.Y {
			// Comparing left-most X of b1 (pivot) to right-most X
			// of b2. If they align, then left-most X of b1 becomes
			// left-most of B2.
			if b1.P1.X == b2.P2.X+1 {
				b1.P1.X = b2.P1.X
				return b1, true
			}
			// Likewise, compare right-most X of b1 to left-most X
			// of b2 and merge.
			if b1.P2.X == b2.P1.X-1 {
				b1.P2.X = b2.P2.X
				return b1, true
			}
		}
	} else {
		// East/West logic path. X coords must match.
		if b1.P1.X == b2.P1.X {
			// Compare top-most Y of b1 to bottom-most Y of b2 and merge.
			if b1.P1.Y == b2.P2.Y+1 {
				b1.P1.Y = b2.P1.Y
				return b1, true
			}
			// Compare bottom-most Y of b1 to top-most Y of b2 and merge.
			if b1.P2.Y == b2.P1.Y-1 {
				b1.P2.Y = b2.P2.Y
				return b1, true
			}
		}
	}

	return zeroB, false
}

func printGrid(grid Grid) {
	for _, row := range grid {
		println(string(row))
	}
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
