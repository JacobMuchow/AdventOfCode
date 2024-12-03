package day03pt1

import (
	"fmt"
	"regexp"

	"github.com/JacobMuchow/AdventOfCode/2024/utils"
)

func Run() {
	lines := utils.ReadLinesFromFile("resources/day03_input.txt")

	regex, ok := regexp.Compile(`mul\((\d{1,3}),(\d{1,3})\)`)
	if ok != nil {
		panic("Failed to compile regex")
	}

	sumTotal := 0

	for _, line := range lines {
		tokens := regex.FindAllStringSubmatch(line, -1)
		if tokens == nil {
			panic("Failed to match from line")
		}

		for _, token := range tokens {
			a := utils.ParseInt(token[1])
			b := utils.ParseInt(token[2])

			sumTotal += a * b
		}
	}

	fmt.Println("Sum total:", sumTotal)
}
