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
	lines := utils.ReadLinesFromFile("resources/day09_input.txt")
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

	for cur := list.head.next; cur != list.tail; cur = cur.next {
		if cur.value != -1 {
			sum += cur.value * i
		}
		i++
	}

	return sum
}

func highestID(list *LinkedList) int {
	for cur := list.tail.prev; cur != list.head; cur = cur.prev {
		if cur.value != -1 {
			return cur.value
		}
	}
	panic("No file IDs found")
}

func segmentStart(list *LinkedList, end *Node) (*Node, int) {
	size := 1

	// Seek prev nodes until value changes
	cur := end
	for {
		if cur.prev.value != end.value || cur.prev == list.head {
			break

		}
		cur = cur.prev
		size += 1
	}

	return cur, size
}

func segmentEnd(list *LinkedList, start *Node) (*Node, int) {
	size := 1
	cur := start

	for {
		if cur.next.value != start.value || cur.next == list.tail {
			break
		}
		size += 1
		cur = cur.next
	}
	return cur, size
}

func tryMoveLeft(list *LinkedList, fileEnd *Node) {
	fileId := fileEnd.value
	fileStart, fileSize := segmentStart(list, fileEnd)

	for cur := list.head.next; cur != fileStart && cur != list.tail; cur = cur.next {
		if cur.value == -1 {
			_, emptySize := segmentEnd(list, cur)

			if emptySize >= fileSize {
				// Instead of editing the LinkedList, we will swap values.
				fileItr := fileStart
				emptyItr := cur

				for i := 0; i < fileSize; i++ {
					emptyItr.value = fileId
					fileItr.value = -1

					emptyItr = emptyItr.next
					fileItr = fileItr.next
				}
				return
			}
		}
	}
}

func optimize(list *LinkedList) {
	curId := highestID(list)

	for cur := list.tail.prev; cur != list.head && curId >= 0; cur = cur.prev {
		if cur.value == curId {
			tryMoveLeft(list, cur)
			curId--
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
