//
//  Day09Pt1.swift
//  Advent
//
//  Created by Jacob Muchow on 11/28/24.
//

import Foundation

class Day09Pt1 {
    static func run() {
        let lines = IOUtils.readLinesFromFile("day09_input.txt")
        let input = lines[0]
        
        let cleanedInput = removeGarbage(input)
        
        let score = scoreGroups(cleanedInput)
        print("Score: \(score)")
    }
    
    static func scoreGroups(_ input: String) -> Int {
        var idx = input.startIndex
        var score = 0
        var depth = 0
        
        while idx < input.endIndex {
            if input[idx] == "{" {
                depth += 1
                score += depth
            } else if input[idx] == "}" {
                depth -= 1
            }
            idx = input.index(after: idx)
        }
        
        return score
    }
    
    static func removeGarbage(_ input: String) -> String {
        var output = input
        var idx = output.startIndex
        
        var garbaseStart: String.Index?
        
        while idx < output.endIndex {
            // Iterate until garbase is detected "<", at which point we set a start index.
            if garbaseStart == nil {
                if output[idx] == "<" {
                    garbaseStart = idx
                } else {
                    // continue
                }
            }
            
            // If garbage has been detected, we iterate until we hit a valid end char ">".
            // Then create a new copy of the output with the garbage sliced out.
            else {
                if output[idx] == ">" {
                    // Create new string with all characters removed between the garbase start & end index, inclusive.
                    // The index in the new copy of the string needs to be recalculated using an offset from the beginning.
                    // We can set it up to start back up wherever the garbase started previously.
                    let garbageOffset = output.distance(from: output.startIndex, to: garbaseStart!)
                    output = output.replacingCharacters(in: garbaseStart!...idx, with: "")
                    idx = output.index(output.startIndex, offsetBy: garbageOffset)
                    garbaseStart = nil
                    continue
                } else if output[idx] == "!" {
                    // Ignore the next character.
                    idx = output.index(idx, offsetBy: 2)
                    continue
                }
            }
            
            idx = output.index(after: idx)
        }
        
        return output
    }
}
