//
//  Day17Pt1.swift
//  Advent
//
//  Created by Jacob Muchow on 11/30/24.
//

import Foundation

class Day17Pt1 {
    static func run() {
        let lines = IOUtils.readLinesFromFile("day17_input.txt")
        let stepCount = Int(lines[0])!
        
        print("Step count: \(stepCount)")
        
        var buffer = [0]
        var currentPos = 0
        
        for i in 1...2017 {
            // Step forward (with some optimizations & circular list logic).
            var stepsLeft = stepCount
            let disToEnd = buffer.count - 1 - currentPos
            
            if stepsLeft > disToEnd {
                stepsLeft -= (disToEnd+1)
                currentPos = 0
            }
            
            stepsLeft = stepsLeft % buffer.count
            currentPos += stepsLeft
            
            buffer.insert(i, at: currentPos+1)
            currentPos += 1
        }
        
        let valueAfter = buffer[currentPos+1]
        print("Value after last insert: \(valueAfter)")
    }
}
