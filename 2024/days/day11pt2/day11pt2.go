package day11pt2

import (
	"fmt"
	"strconv"
	"strings"

	"github.com/JacobMuchow/AdventOfCode/2024/utils"
	"github.com/JacobMuchow/AdventOfCode/2024/utils/linkedlist"
)

type StoneList = linkedlist.LinkedList[string]

func Run() {
	lines := utils.ReadLinesFromFile("resources/day11_test.txt")
	stones := parseStones(lines[0])

	for i := range 10 {
		fmt.Print("Iter ", i, ": ")
		stones.PrintValues(" ")
		fmt.Println("\n")
		stones = blink(stones)
	}
	fmt.Println("Num stones:", stones.Len())
}

func parseStones(line string) *StoneList {
	fields := strings.Fields(line)

	list := linkedlist.New[string]()
	prev := list.Head

	for _, stone := range fields {
		prev = list.Insert(stone, prev)
	}

	prev.Next = list.Tail
	list.Tail.Prev = prev
	return list
}

func blink(stones *StoneList) *StoneList {
	cur := stones.First()

	for cur != stones.Tail {
		stone := cur.Value

		// Rule 1
		if stone == "0" {
			cur.Value = "1"
			cur = cur.Next
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

			cur.Value = stoneA
			newStone := stones.Insert(stoneB, cur)
			cur = newStone.Next
			continue
		}

		// Rule 3
		value := utils.ParseInt(stone) * 2024
		cur.Value = strconv.Itoa(value)
		cur = cur.Next
	}

	return stones
}
