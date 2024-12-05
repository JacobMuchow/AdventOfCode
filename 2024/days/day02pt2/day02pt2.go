package day02pt2

import (
	"fmt"
	"strings"

	"github.com/JacobMuchow/AdventOfCode/2024/utils"
	"github.com/JacobMuchow/AdventOfCode/2024/utils/arrays"
)

func Run() {
	lines := utils.ReadLinesFromFile("resources/day02_input.txt")

	// Parse reports into list.
	reports := make([][]int, len(lines))
	for i, line := range lines {
		fields := strings.Fields(line)
		levels := make([]int, len(fields))

		for j, field := range fields {
			level := utils.ParseInt(field)
			levels[j] = level
		}

		reports[i] = levels
	}

	// Evaluate & count up number of safe reports.
	numSafe := 0
	for _, report := range reports {
		if isSafe(report) {
			numSafe += 1
		} else {
			// If the initial report is not safe, try removing 1 level
			// at each index until it is safe (pt2 "dampener").
			for i := 0; i < len(report); i++ {
				reportCopy := arrays.RemovingIndex(report, i)
				if isSafe(reportCopy) {
					numSafe += 1
					break
				}
			}
		}
	}

	fmt.Println("Num safe: ", numSafe)
}

func isSafe(report []int) bool {
	asc := report[1]-report[0] > 0

	for i := 0; i < len(report)-1; i++ {
		// Reverse how we consider the "delta" based on ascending or descending list.
		var delta int
		if asc {
			delta = report[i+1] - report[i]
		} else {
			delta = report[i] - report[i+1]
		}

		// Negative values are a change in the wrong direction.
		// 0 delta means same number.
		// > 3 is correct direction, but too large of a change.
		if delta < 1 || delta > 3 {
			return false
		}
	}

	return true
}
