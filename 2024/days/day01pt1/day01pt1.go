package day01pt1

import (
	"fmt"
	"sort"
	"strings"

	"github.com/JacobMuchow/AdventOfCode/2024/utils"
)

func Run() {
	lines := utils.ReadLinesFromFile("resources/day01_input.txt")

	listA := make([]int, len(lines))
	listB := make([]int, len(lines))

	for i, line := range lines {
		fields := strings.Fields(line)

		num1 := utils.ParseInt(fields[0])
		num2 := utils.ParseInt(fields[1])

		listA[i] = num1
		listB[i] = num2
	}

	sort.Ints(listA)
	sort.Ints(listB)

	sum := 0
	for i := 0; i < len(listA); i++ {
		sum += utils.Abs(listA[i] - listB[i])
	}

	fmt.Println("Diff sum:", sum)
}
