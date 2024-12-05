package arrays

// MoveValue moves the value at `fromIndex` to `toIndex` in the array `arr`.
func MoveValue(arr []int, fromIndex int, toIndex int) []int {
	// Remove the value from the original index
	value := arr[fromIndex]
	arr = append(arr[:fromIndex], arr[fromIndex+1:]...)

	// Insert the value at the new index
	if toIndex >= len(arr) {
		arr = append(arr, value)
	} else {
		arr = append(arr[:toIndex], append([]int{value}, arr[toIndex:]...)...)
	}

	return arr
}
