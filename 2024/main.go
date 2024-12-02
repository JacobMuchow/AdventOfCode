package main

import (
	"fmt"
	"time"

	days "github.com/JacobMuchow/AdventOfCode/2024/days"
)

func runChallenge(routine func()) {
	start := time.Now()
	routine()
	time_taken := time.Since(start)
	fmt.Printf("Time taken: %v\n", time_taken)
}

func main() {
	runChallenge(days.Day01Pt2)
}
