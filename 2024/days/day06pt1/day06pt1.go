package day06pt1

import (
	"fmt"

	"github.com/JacobMuchow/AdventOfCode/2024/utils"
)

type Rules = map[string]bool

func Run() {
	lines := utils.ReadLinesFromFile("resources/day06_test.txt")

	for _, line := range lines {
		fmt.Println(line)
	}
}
