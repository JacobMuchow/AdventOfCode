package day07pt2

import (
	"fmt"
	"strconv"
	"strings"

	"github.com/JacobMuchow/AdventOfCode/2024/utils"
)

func Run() {
	lines := utils.ReadLinesFromFile("resources/day07_input.txt")

	sumTotal := 0

	for _, line := range lines {
		sum, operands := parseLine(line)

		if isPossible(sum, 0, operands) {
			sumTotal += sum
		}
	}

	fmt.Println("Sum total:", sumTotal)
}

func isPossible(expected int, cur int, operands []int) bool {
	if cur > expected {
		return false
	}

	if len(operands) == 0 {
		return cur == expected
	}

	return isPossible(expected, cur*operands[0], operands[1:]) ||
		isPossible(expected, cur+operands[0], operands[1:]) ||
		isPossible(expected, concat(cur, operands[0]), operands[1:])
}

func concat(cur int, operator int) int {
	return utils.ParseInt(strconv.Itoa(cur) + strconv.Itoa(operator))
}

func parseLine(line string) (int, []int) {
	fields := strings.Fields(line)

	sum := utils.ParseInt(fields[0][:len(fields[0])-1])

	operands := make([]int, len(fields)-1)

	for i := 1; i < len(fields); i++ {
		operands[i-1] = utils.ParseInt(fields[i])
	}

	return sum, operands
}
