package main

import (
	"fmt"
	"time"
)

func day01() {
	fmt.Println("Day 01")
}

func runChallenge(routine func()) {
	start := time.Now()
	routine()
	time_taken := time.Since(start)
	fmt.Printf("Time taken: %v\n", time_taken)
}

func main() {
	runChallenge(day01)
}
