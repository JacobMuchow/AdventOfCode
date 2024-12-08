package main

import (
	"fmt"
	"time"

	"github.com/JacobMuchow/AdventOfCode/2024/days/day08pt1"
)

func main() {
	start := time.Now()
	day08pt1.Run()
	time_taken := time.Since(start)
	fmt.Printf("Time taken: %v\n", time_taken)
}
