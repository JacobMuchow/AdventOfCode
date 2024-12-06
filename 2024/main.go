package main

import (
	"fmt"
	"time"

	"github.com/JacobMuchow/AdventOfCode/2024/days/day06pt2"
)

func main() {
	start := time.Now()
	day06pt2.Run()
	time_taken := time.Since(start)
	fmt.Printf("Time taken: %v\n", time_taken)
}
