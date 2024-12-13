package day09pt1

import (
	"github.com/JacobMuchow/AdventOfCode/2024/utils"
	"github.com/JacobMuchow/AdventOfCode/2024/utils/arrays"
)

type Segment struct {
	fileId int
	size   int
}

func Run() {
	lines := utils.ReadLinesFromFile("resources/day09_test.txt")
	input := lines[0]

	segments := parseSegments(input)

	for i := 0; i < len(segments); {
		if segments[i].fileId != -1 {
			i +=1
			continue
		}


	}
}

func fillEmptySegment(segments []Segment, pos int) []Segment {
	emptySeg := segments[pos]

	movedSegs := make([]Segment, 0)
	for i := pos+1; i < len(segments); i++ {
		if 
	}
}

func parseSegments(input string) []Segment {
	runes := []rune(input)

	segments := make([]Segment, len(runes))
	isEmpty := false

	for i, char := range runes {
		fileId := -1
		if !isEmpty {
			fileId = i / 2
		}

		segments[i] = Segment{
			fileId: fileId,
			size:   utils.ParseInt(string(char)),
		}

		isEmpty = !isEmpty
	}

	return segments
}
