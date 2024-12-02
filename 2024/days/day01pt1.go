package days

import (
	"fmt"

	"github.com/JacobMuchow/AdventOfCode/2024/utils"
)

func Day01Pt1() {
	lines := utils.ReadLinesFromFile("resources/day01_test.txt")
	for _, line := range lines {
		fmt.Println(line)
	}
}
