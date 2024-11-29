//
//  Day10Pt1.swift
//  Advent
//
//  Created by Jacob Muchow on 11/29/24.
//

import Foundation

class Day10Pt1 {
    static func run() {
        let lines = IOUtils.readLinesFromFile("day10_input.txt")
        let listSize = Int(lines[0])!
        let inputs = lines[1].split(separator: ",").map({ Int($0)! })
        
        var list = Array(0..<listSize)
        print("List: \(list)")
        
        print("Inputs: \(inputs)")
        
        var curIdx = 0
        var skipSize = 0
        
        for length in inputs {
            var i = curIdx
            var j = curIdx + length - 1
            
            while i < j {
                let iSafe = i % listSize
                let jSafe = j % listSize
                
                let swap = list[iSafe]
                list[iSafe] = list[jSafe]
                list[jSafe] = swap
                
                i += 1
                j -= 1
            }
            
            curIdx = (curIdx + length + skipSize) % listSize
            skipSize += 1
        }
        
        let result = list[0] * list[1]
        print("Result: \(result)")
    }
}
