package day05pt2

import (
	"fmt"
	"strings"

	"github.com/JacobMuchow/AdventOfCode/2024/utils"
)

type Rules = map[string]bool

func Run() {
	lines := utils.ReadLinesFromFile("resources/day05_test.txt")

	rules, updates := parseInput(lines)

	sum := 0
	for _, update := range updates {
		if updateIsValid(update, rules) {
			sum += update[len(update)/2]
		}
	}

	fmt.Println("Valid update sum:", sum)
}

func updateIsValid(update []int, rules Rules) bool {
	// For all combinations, check if there is a rule that they should actually
	// be in the reverse order.
	for i := 0; i < len(update)-1; i++ {
		for j := i + 1; j < len(update); j++ {
			rule := fmt.Sprintf("%d|%d", update[j], update[i])
			if rules[rule] {
				return false
			}
		}
	}

	return true
}

func parseInput(lines []string) (Rules, [][]int) {
	rules := make(Rules, 0)
	updates := make([][]int, 0)

	// First parse the rules. When empty line is hit,
	// this is changed to false and we parse the update lists.
	parsing_rules := true

	for _, line := range lines {
		if len(line) == 0 {
			parsing_rules = false
			continue
		}

		if parsing_rules {
			rules[line] = true
		} else {
			tokens := strings.Split(line, ",")
			update := make([]int, len(tokens))
			for i, token := range tokens {
				update[i] = utils.ParseInt(token)
			}
			updates = append(updates, update)
		}
	}

	return rules, updates
}
