package arrays

func RemovingIndex(s []int, index int) []int {
	newArray := make([]int, len(s))
	copy(newArray, s)

	if index == len(newArray)-1 {
		return newArray[:index]
	}

	return append(newArray[:index], newArray[index+1:]...)
}
