package day01pt2

import (
	"fmt"
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

	listBMap := make(map[int]int, len(listB))
	for _, num := range listB {
		listBMap[num] = listBMap[num] + 1
	}

	score := 0
	for i := 0; i < len(listA); i++ {
		score += listA[i] * listBMap[listA[i]]
	}

	fmt.Println("Similarity sum:", score)
}
