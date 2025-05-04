package linkedlist

import "fmt"

type LinkedList[T any] struct {
	Head *Node[T]
	Tail *Node[T]
}

type Node[T any] struct {
	Value T
	Prev  *Node[T]
	Next  *Node[T]
}

func New[T any]() *LinkedList[T] {
	list := &LinkedList[T]{}
	list.Head = &Node[T]{}
	list.Tail = &Node[T]{}
	list.Head.Next = list.Tail
	list.Tail.Prev = list.Head
	return list
}

func (list *LinkedList[T]) First() *Node[T] {
	return list.Head.Next
}

func (list *LinkedList[T]) Last() *Node[T] {
	return list.Tail.Prev
}

func (list *LinkedList[T]) Insert(value T, after *Node[T]) *Node[T] {
	new := Node[T]{Value: value}

	before := after.Next

	before.Prev = &new
	new.Next = before

	after.Next = &new
	new.Prev = after

	return &new
}

func (list *LinkedList[T]) Move(seg *Node[T], after *Node[T]) {
	seg.Prev.Next = seg.Next
	seg.Next.Prev = seg.Prev

	before := after.Next
	before.Prev = seg
	after.Next = seg

	seg.Prev = after
	seg.Next = before
}

func (list *LinkedList[T]) Len() int {
	count := 0

	cur := list.Head.Next
	for cur != list.Tail {
		count++
		cur = cur.Next
	}

	return count
}

func (list *LinkedList[T]) PrintValues(separator string) {
	cur := list.First()

	for {
		fmt.Print(cur.Value)
		cur = cur.Next

		if cur == list.Tail {
			break
		} else {
			fmt.Print(separator)
		}
	}
	fmt.Println("")
}
