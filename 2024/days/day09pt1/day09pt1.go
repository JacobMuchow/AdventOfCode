package day09pt1

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
	visualize(list)
	optimize(list)

	// listMove(list.tail.prev, list.head.next)
	visualize(list)
}

func optimize(list *LinkedList) {
	left := list.head.next
	right := list.tail.prev

	for ; left != right; left = left.next {
		if left.value == -1 {
			for ; right != left; right = right.prev {
				if right.value != -1 {
					prev := right.prev
					listMove(right, left)
					listMove(left, prev)

					swap := left
					left = right
					right = swap

					visualize(list)
					break
				}
			}
		}
	}
}

func fillEmpty(list *LinkedList, seg *Node) *Node {
	for cur := list.tail.prev; cur != seg; cur = cur.prev {
		if cur.value != -1 {
			prev := cur.prev
			listMove(cur, seg)
			listMove(seg, prev)
			return cur
		}
	}
	return nil
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
