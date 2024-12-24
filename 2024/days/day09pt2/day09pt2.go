package day09pt2

import (
	"fmt"

	"github.com/JacobMuchow/AdventOfCode/2024/utils"
	"github.com/JacobMuchow/AdventOfCode/2024/utils/linkedlist"
)

type LinkedList = linkedlist.LinkedList[int]
type Node = linkedlist.Node[int]

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

	for cur := list.Head.Next; cur != list.Tail; cur = cur.Next {
		if cur.Value != -1 {
			sum += cur.Value * i
		}
		i++
	}

	return sum
}

func highestID(list *LinkedList) int {
	for cur := list.Tail.Prev; cur != list.Head; cur = cur.Prev {
		if cur.Value != -1 {
			return cur.Value
		}
	}
	panic("No file IDs found")
}

func segmentStart(list *LinkedList, end *Node) (*Node, int) {
	size := 1

	// Seek prev nodes until value changes
	cur := end
	for {
		if cur.Prev.Value != end.Value || cur.Prev == list.Head {
			break

		}
		cur = cur.Prev
		size += 1
	}

	return cur, size
}

func segmentEnd(list *LinkedList, start *Node) (*Node, int) {
	size := 1
	cur := start

	for {
		if cur.Next.Value != start.Value || cur.Next == list.Tail {
			break
		}
		size += 1
		cur = cur.Next
	}
	return cur, size
}

func tryMoveLeft(list *LinkedList, fileEnd *Node) {
	fileId := fileEnd.Value
	fileStart, fileSize := segmentStart(list, fileEnd)

	for cur := list.Head.Next; cur != fileStart && cur != list.Tail; cur = cur.Next {
		if cur.Value == -1 {
			_, emptySize := segmentEnd(list, cur)

			if emptySize >= fileSize {
				// Instead of editing the LinkedList, we will swap values.
				fileItr := fileStart
				emptyItr := cur

				for i := 0; i < fileSize; i++ {
					emptyItr.Value = fileId
					fileItr.Value = -1

					emptyItr = emptyItr.Next
					fileItr = fileItr.Next
				}
				return
			}
		}
	}
}

func optimize(list *LinkedList) {
	curId := highestID(list)

	for cur := list.Tail.Prev; cur != list.Head && curId >= 0; cur = cur.Prev {
		if cur.Value == curId {
			tryMoveLeft(list, cur)
			curId--
		}
	}
}

func visualize(list *LinkedList) {
	for cur := list.Head.Next; cur != list.Tail; cur = cur.Next {
		if cur.Value == -1 {
			fmt.Printf(".")
		} else {
			fmt.Printf("%d", cur.Value)
		}
	}
	fmt.Println()
}

func parseSegments(input string) *LinkedList {
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
