package day03pt2

import (
	"fmt"
	"regexp"

	"github.com/JacobMuchow/AdventOfCode/2024/utils"
)

func Run() {
	lines := utils.ReadLinesFromFile("resources/day03_input.txt")

	regex, ok := regexp.Compile(`mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don't\(\)`)
	if ok != nil {
		panic("Failed to compile regex")
	}

	sumTotal := 0
	mulEnabled := true

	for _, line := range lines {
		matches := regex.FindAllStringSubmatch(line, -1)
		if matches == nil {
			panic("Failed to match from line")
		}

		for _, match := range matches {
			switch match[0] {
			case "do()":
				mulEnabled = true
			case "don't()":
				mulEnabled = false
			default:
				if mulEnabled {
					a := utils.ParseInt(match[1])
					b := utils.ParseInt(match[2])

					sumTotal += a * b
				}
			}
		}
	}

	fmt.Println("Sum total:", sumTotal)
}
