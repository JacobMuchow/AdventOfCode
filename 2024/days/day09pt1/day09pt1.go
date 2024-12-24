package day09pt1

import (
	"fmt"

	"github.com/JacobMuchow/AdventOfCode/2024/utils"
	"github.com/JacobMuchow/AdventOfCode/2024/utils/linkedlist"
)

type MemList = linkedlist.LinkedList[int]

func Run() {
	lines := utils.ReadLinesFromFile("resources/day09_input.txt")
	input := lines[0]

	list := parseSegments(input)
	// visualize(list)
	optimize(list)
	// visualize(list)

	checksum := checksum(list)
	fmt.Println("Checksum:", checksum)
}

func checksum(list *MemList) int {
	sum := 0
	i := 0
	cur := list.Head.Next

	for cur != list.Tail && cur.Value != -1 {
		sum += cur.Value * i

		i++
		cur = cur.Next
	}

	return sum
}

func optimize(list *MemList) {
	// We can traverse using a left and right pointer. Swapping empty elements from the left
	// with next non-empty element from the right. When the pointers meet, we are done.
	left := list.Head.Next
	right := list.Tail.Prev

	// Move left pointer in until we find empty space.
	for ; left != right; left = left.Next {
		if left.Value == -1 {
			// Once empty space is found, move right pointer in until we find non-empty space.
			for ; right != left; right = right.Prev {
				if right.Value != -1 {
					// Swap the nodes positions in the LinkedList.
					prev := right.Prev
					list.Move(right, left)
					list.Move(left, prev)

					// Don't forget we will need to swap our left & right pointers.
					swap := left
					left = right
					right = swap
					break
				}
			}
		}
	}
}

func visualize(list *MemList) {
	for cur := list.Head.Next; cur != list.Tail; cur = cur.Next {
		if cur.Value == -1 {
			fmt.Printf(".")
		} else {
			fmt.Printf("%d", cur.Value)
		}
	}
	fmt.Println()
}

func parseSegments(input string) *MemList {
	list := linkedlist.New[int]()

	prev := list.Head
	isEmpty := false

	for i, char := range input {
		size := utils.ParseInt(string(char))
		value := -1
		if !isEmpty {
			value = i / 2
		}

		for i := 0; i < size; i++ {
			prev = list.Insert(value, prev)
		}

		isEmpty = !isEmpty
	}

	prev.Next = list.Tail
	list.Tail.Prev = prev

	return list
}
