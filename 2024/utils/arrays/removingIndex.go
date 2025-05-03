package arrays

func RemovingIndex[T any](s []T, index int) []T {
	newArray := make([]T, len(s))
	copy(newArray, s)

	if index == len(newArray)-1 {
		return newArray[:index]
	}

	return append(newArray[:index], newArray[index+1:]...)
}
