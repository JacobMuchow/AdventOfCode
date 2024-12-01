package main

import (
	"fmt"
	"time"

	"github.com/JacobMuchow/AdventOfCode/2024/day01"
)

func runChallenge(routine func()) {
	start := time.Now()
	routine()
	time_taken := time.Since(start)
	fmt.Printf("Time taken: %v\n", time_taken)
}

func main() {
	runChallenge(day01.Pt1)
}
