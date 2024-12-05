package arrays

func IndexOf[T comparable](array []T, val T) int {
	for i, itemVal := range array {
		if itemVal == val {
			return i
		}
	}
	return -1
}
