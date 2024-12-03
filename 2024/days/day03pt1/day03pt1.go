package day03pt1

import (
	"fmt"

	"github.com/JacobMuchow/AdventOfCode/2024/utils"
)

func Run() {
	lines := utils.ReadLinesFromFile("resources/day03_input.txt")

	// Parse reports into list.
	for _, line := range lines {
		fmt.Println(line)
	}
}
