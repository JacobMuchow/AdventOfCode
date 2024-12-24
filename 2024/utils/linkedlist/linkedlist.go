package linkedlist

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
