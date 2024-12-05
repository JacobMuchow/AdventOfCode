package day05pt1

import (
	"fmt"

	"github.com/JacobMuchow/AdventOfCode/2024/utils"
)

func Run() {
	lines := utils.ReadLinesFromFile("resources/day05_test.txt")

	for _, line := range lines {
		fmt.Println(line)
	}
}
