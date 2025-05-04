package day11pt1

import (
	"fmt"
	"strconv"
	"strings"

	"github.com/JacobMuchow/AdventOfCode/2024/utils"
	"github.com/JacobMuchow/AdventOfCode/2024/utils/arrays"
)

func Run() {
	lines := utils.ReadLinesFromFile("resources/day11_input.txt")
	stones := parseStones(lines[0])

	for i := 0; i < 25; i++ {
		fmt.Println("Iter", i)
		stones = blink(stones)
	}
	fmt.Println("Num stones:", len(stones))
}

func parseStones(line string) []string {
	fields := strings.Fields(line)
	return fields
}

func blink(stones []string) []string {
	for i := 0; i < len(stones); i++ {
		stone := stones[i]

		// Rule 1
		if stone == "0" {
			stones[i] = "1"
			continue
		}

		// Rule 2
		numDigits := len(stone)
		if numDigits%2 == 0 {
			stoneA := stone[:numDigits/2]
			stoneB := stone[numDigits/2:]

			// Clean up the preceding 0's.
			stoneA = strconv.Itoa(utils.ParseInt(stoneA))
			stoneB = strconv.Itoa(utils.ParseInt(stoneB))

			stones[i] = stoneA
			stones = arrays.Insert(stones, i+1, stoneB)
			i++
			continue
		}

		// Rule 3
		value := utils.ParseInt(stone) * 2024
		stones[i] = strconv.Itoa(value)
	}

	return stones
}
