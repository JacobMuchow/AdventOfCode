package day10pt2

import (
	"fmt"

	"github.com/JacobMuchow/AdventOfCode/2024/utils"
	"github.com/JacobMuchow/AdventOfCode/2024/utils/queue"
)

type Grid = [][]int
type Pos2d struct {
	X int
	Y int
}

type QueueItem struct {
	pos     Pos2d
	lastVal int
}

func Run() {
	lines := utils.ReadLinesFromFile("resources/day10_input.txt")

	grid := parseGrid(lines)
	printGrid(grid)

	trailheads := findTrailheads(grid)
	fmt.Println("Trailheads:", trailheads)

	totalScore := 0
	for _, trailhead := range trailheads {
		endings := findEndings(grid, trailhead)
		totalScore += len(endings)
	}

	fmt.Println("Total score:", totalScore)
}

func findTrailheads(grid Grid) []Pos2d {
	trailheads := make([]Pos2d, 0, 1)
	for y, row := range grid {
		for x, val := range row {
			if val == 0 {
				trailheads = append(trailheads, Pos2d{x, y})
			}
		}
	}
	return trailheads
}

func findEndings(grid Grid, trailhead Pos2d) []Pos2d {
	endings := make([]Pos2d, 0)

	// visited := make(map[string]bool, 0)
	queue := queue.New[QueueItem]()
	queue.Push(QueueItem{trailhead, -1})

	for !queue.IsEmpty() {
		item, _ := queue.Pop()
		x := item.pos.X
		y := item.pos.Y

		if x < 0 || x >= len(grid[0]) || y < 0 || y >= len(grid) {
			continue
		}

		curVal := grid[y][x]
		if curVal != item.lastVal+1 {
			continue
		}

		// key := posKey(item.pos)
		// if visited[key] {
		// 	continue
		// }
		// visited[key] = true

		if curVal == 9 {
			endings = append(endings, item.pos)
			continue
		}

		queue.Push(QueueItem{Pos2d{x + 1, y}, curVal})
		queue.Push(QueueItem{Pos2d{x - 1, y}, curVal})
		queue.Push(QueueItem{Pos2d{x, y + 1}, curVal})
		queue.Push(QueueItem{Pos2d{x, y - 1}, curVal})
	}

	return endings
}

func parseGrid(lines []string) Grid {
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

	return grid
}

func printGrid(grid Grid) {
	for _, row := range grid {
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

func posKey(pos Pos2d) string {
	return fmt.Sprintf("%d,%d", pos.X, pos.Y)
}
