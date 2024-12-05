package day05pt2

import (
	"fmt"
	"strings"

	"github.com/JacobMuchow/AdventOfCode/2024/utils"
	"github.com/JacobMuchow/AdventOfCode/2024/utils/arrays"
)

type Rules = map[string]bool

func Run() {
	lines := utils.ReadLinesFromFile("resources/day05_input.txt")

	rules, updates := parseInput(lines)

	//  Find invalid updates.
	invalid_updates := make([][]int, 0, len(lines))
	for _, update := range updates {
		if failedRule(update, rules) != "" {
			invalid_updates = append(invalid_updates, update)
		}
	}

	// Fix each update, then sum up the middle values in the fixed list.
	sum := 0
	for i, update := range invalid_updates {
		fmt.Println(i)
		fixed_update := fixUpdate(update, rules)
		sum += update[len(fixed_update)/2]
	}

	fmt.Println("Sum of fixed updates:", sum)
}

func fixUpdate(update []int, rules Rules) []int {
	for {
		// Check for failed rule, then update. As soon as there isn't
		// one break the loop.
		rule := failedRule(update, rules)
		if rule == "" {
			return update
		}

		tokens := strings.Split(rule, "|")
		valA := utils.ParseInt(tokens[0])
		valB := utils.ParseInt(tokens[1])

		idxA := arrays.IndexOf(update, valA)
		idxB := arrays.IndexOf(update, valB)

		update = arrays.MoveValue(update, idxB, idxA)
	}
}

func failedRule(update []int, rules Rules) string {
	// For all combinations, check if there is a rule that they should actually
	// be in the reverse order.
	for i := 0; i < len(update)-1; i++ {
		for j := i + 1; j < len(update); j++ {
			rule := fmt.Sprintf("%d|%d", update[j], update[i])
			if rules[rule] {
				return rule
			}
		}
	}

	return ""
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
