package queue

import "github.com/JacobMuchow/AdventOfCode/2024/utils/arrays"

type Queue[T any] struct {
	items []T
}

func New[T any]() *Queue[T] {
	return &Queue[T]{}
}

func (queue *Queue[T]) Size() int {
	return len(queue.items)
}

func (queue *Queue[T]) IsEmpty() bool {
	return len(queue.items) == 0
}

func (queue *Queue[T]) Push(item T) {
	queue.items = append(queue.items, item)
}

func (queue *Queue[T]) Pop() (T, bool) {
	if queue.IsEmpty() {
		var zero T
		return zero, false
	}

	popped := queue.items[0]
	queue.items = arrays.RemovingIndex(queue.items, 0)
	return popped, true
}
