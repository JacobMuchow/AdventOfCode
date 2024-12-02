//
//  Day17Pt2.swift
//  Advent
//
//  Created by Jacob Muchow on 11/30/24.
//

import Foundation

class Day17Pt2 {
    static func run() {
        let lines = IOUtils.readLinesFromFile("day17_input.txt")
        let stepCount = Int(lines[0])!
        
        print("Step count: \(stepCount)")
        
        // Instead of _actually_ maintaining a buffer (too slow), we will simulate one.
        var bufferSize = 1
        var currentPos = 0
        var lastValueAtPos1 = 0
        
        while bufferSize <= 50_000_000 {
            if bufferSize % 1_000_000 == 0 {
                print("Loop \(bufferSize)")
            }
            
            // Step forward (with some optimizations & circular list logic).
            var stepsLeft = stepCount
            let disToEnd = bufferSize - 1 - currentPos
            
            if stepsLeft > disToEnd {
                stepsLeft -= (disToEnd+1)
                currentPos = 0
            }
            
            stepsLeft = stepsLeft % bufferSize
            currentPos += stepsLeft
            
            // Where we would normally do an insert, just track the last value we would have added
            // when we are at pos 0.
//            buffer.insert(i, at: currentPos+1)
            if currentPos == 0 {
                lastValueAtPos1 = bufferSize
            }
            currentPos += 1
            bufferSize += 1
        }
        
        print("Value at pos 1: \(lastValueAtPos1)")
    }
}
