package day09pt1

import (
	"fmt"

	"github.com/JacobMuchow/AdventOfCode/2024/utils"
)

type LinkedList struct {
	head *Segment
	tail *Segment
}

type Segment struct {
	fileId int
	size   int
	empty  bool

	prev *Segment
	next *Segment
}

func Run() {
	lines := utils.ReadLinesFromFile("resources/day09_test.txt")
	input := lines[0]

	list := parseSegments(input)
	visualize(list)
}

func visualize(list *LinkedList) {
	for cur := list.head.next; cur != list.tail; cur = cur.next {
		for i := 0; i < cur.size; i++ {
			if cur.empty {
				fmt.Printf(".")
			} else {
				fmt.Printf("%d", cur.fileId)
			}
		}
	}
}

func parseSegments(input string) *LinkedList {
	runes := []rune(input)

	head := &Segment{fileId: -1, empty: true, size: 0}
	tail := &Segment{fileId: -1, empty: true, size: 0}
	prev := head

	isEmpty := false

	for i, char := range runes {
		fileId := -1
		if !isEmpty {
			fileId = i / 2
		}

		segment := Segment{
			fileId: fileId,
			empty:  isEmpty,
			size:   utils.ParseInt(string(char)),
		}

		segment.prev = prev
		prev.next = &segment

		isEmpty = !isEmpty
		prev = &segment
	}

	prev.next = tail
	tail.prev = prev

	return &LinkedList{head, tail}
}
