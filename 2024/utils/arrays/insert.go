package arrays

func Insert[T any](arr []T, index int, value T) []T {
	if index >= len(arr) {
		arr = append(arr, value)
	} else {
		arr = append(arr[:index], append([]T{value}, arr[index:]...)...)
	}

	return arr
}
