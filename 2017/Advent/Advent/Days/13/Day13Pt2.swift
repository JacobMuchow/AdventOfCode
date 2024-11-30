//
//  Day13Pt2.swift
//  Advent
//
//  Created by Jacob Muchow on 11/29/24.
//

import Foundation

class Day13Pt2 {
    static func run() {
        let lines = IOUtils.readLinesFromFile("day13_input.txt")
        
        let scanners = parseScanners(from: lines)
        
        for (depth, range) in scanners {
            print("\(depth) -> \(range)")
        }
        
        let maxDepth = scanners.keys.max()!
        print("Max depth: \(maxDepth)")
        
        var startTime = 0
        while willBeCaught(startingFrom: startTime, scanners: scanners) {
            startTime += 1
        }
        
        print("Minimum time to not get caught: \(startTime)")
    }
    
    static func willBeCaught(startingFrom startTime: Int, scanners: [Int: Int]) -> Bool {
        for (depth, range) in scanners {
            let time = startTime + depth
            let scannerPos = scannerPos(at: time, range: range)
            if (scannerPos == 0) {
                return true
            }
        }
        return false
    }
    
    static func scannerPos(at time: Int, range: Int) -> Int {
        var remainder = time % (range * 2 - 2)
        
        if remainder < range {
            return remainder
        }
        
        remainder = remainder % (range - 1)
        return range - 1 - remainder
    }
    
    static func parseScanners(from lines: [String]) -> [Int: Int] {
        var scanners: [Int: Int] = [:]
        
        for line in lines {
            let parts = line.split(separator: ": ")
            let depth = Int(parts[0])!
            let range = Int(parts[1])!
            
            scanners[depth] = range
        }
        
        return scanners
    }
}
