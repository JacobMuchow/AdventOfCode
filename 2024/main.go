package main

import (
	"fmt"
	"time"

	"github.com/JacobMuchow/AdventOfCode/2024/days/day09pt2"
)

func main() {
	start := time.Now()
	day09pt2.Run()
	time_taken := time.Since(start)
	fmt.Printf("Time taken: %v\n", time_taken)
}
