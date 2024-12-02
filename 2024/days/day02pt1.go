package days

import (
	"fmt"
	"strings"

	"github.com/JacobMuchow/AdventOfCode/2024/utils"
)

func Day02Pt1() {
	lines := utils.ReadLinesFromFile("resources/day02_input.txt")

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

	numSafe := 0

	for _, report := range reports {
		safe := isSafe(report)

		if safe {
			numSafe += 1
		} else {
			for i := 0; i < len(report); i++ {
				reportCopy := removingIndex(report, i)
				safe = isSafe(reportCopy)
				if safe {
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
		delta := report[i] - report[i+1]
		if asc {
			delta = report[i+1] - report[i]
		}

		if delta < 1 || delta > 3 {
			return false
		}
	}

	return true
}

func removingIndex(s []int, index int) []int {
	newArray := make([]int, len(s))
	copy(newArray, s)

	if index == len(newArray)-1 {
		return newArray[:index]
	}

	return append(newArray[:index], newArray[index+1:]...)
}
