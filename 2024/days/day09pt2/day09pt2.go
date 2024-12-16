package day09pt2

import (
	"fmt"

	"github.com/JacobMuchow/AdventOfCode/2024/utils"
)

type LinkedList struct {
	head *Node
	tail *Node
}

type Node struct {
	value int
	prev  *Node
	next  *Node
}

func Run() {
	lines := utils.ReadLinesFromFile("resources/day09_test.txt")
	input := lines[0]

	list := parseSegments(input)
	// visualize(list)
	optimize(list)
	// visualize(list)

	checksum := checksum(list)
	fmt.Println("Checksum:", checksum)
}

func checksum(list *LinkedList) int {
	sum := 0
	i := 0
	cur := list.head.next

	for cur != list.tail && cur.value != -1 {
		sum += cur.value * i

		i++
		cur = cur.next
	}

	return sum
}

func optimize(list *LinkedList) {
	// We can traverse using a left and right pointer. Swapping empty elements from the left
	// with next non-empty element from the right. When the pointers meet, we are done.
	left := list.head.next
	right := list.tail.prev

	// Move left pointer in until we find empty space.
	for ; left != right; left = left.next {
		if left.value == -1 {
			// Once empty space is found, move right pointer in until we find non-empty space.
			for ; right != left; right = right.prev {
				if right.value != -1 {
					// Swap the nodes positions in the LinkedList.
					prev := right.prev
					listMove(right, left)
					listMove(left, prev)

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

func listInsert(value int, after *Node) *Node {
	new := Node{value: value}

	before := after.next

	before.prev = &new
	new.next = before

	after.next = &new
	new.prev = after

	return &new
}

func listMove(seg *Node, after *Node) {
	seg.prev.next = seg.next
	seg.next.prev = seg.prev

	before := after.next
	before.prev = seg
	after.next = seg

	seg.prev = after
	seg.next = before
}

func visualize(list *LinkedList) {
	for cur := list.head.next; cur != list.tail; cur = cur.next {
		if cur.value == -1 {
			fmt.Printf(".")
		} else {
			fmt.Printf("%d", cur.value)
		}
	}
	fmt.Println()
}

func parseSegments(input string) *LinkedList {
	head := &Node{}
	tail := &Node{}

	head.next = tail
	tail.prev = head

	prev := head
	isEmpty := false

	for i, char := range input {
		size := utils.ParseInt(string(char))
		value := -1
		if !isEmpty {
			value = i / 2
		}

		for i := 0; i < size; i++ {
			prev = listInsert(value, prev)
		}

		isEmpty = !isEmpty
	}

	prev.next = tail
	tail.prev = prev

	return &LinkedList{head, tail}
}
