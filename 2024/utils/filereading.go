package utils

import (
	"bufio"
	"log"
	"os"
)

func ReadLinesFromFile(path string) []string {
	file, err := os.Open(path)
	if err != nil {
		log.Fatal("Error opening file:", err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	lines := []string{}

	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}

	if err := scanner.Err(); err != nil {
		log.Fatal("Error reading file:", err)
	}

	return lines
}
