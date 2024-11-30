//
//  Day13Pt2.swift
//  Advent
//
//  Created by Jacob Muchow on 11/29/24.
//

import Foundation

class Day13Pt2 {
    static func run() {
        let lines = IOUtils.readLinesFromFile("day13_test.txt")
        
        let scanners = parseScanners(from: lines)
        
        for (depth, range) in scanners {
            print("\(depth) -> \(range)")
        }
        
        let maxDepth = scanners.keys.max()!
        print("Max depth: \(maxDepth)")
        
        var severity = 0
        
        for curDepth in 0...maxDepth {
            if let scannerRange = scanners[curDepth] {
                let scannerPos = scannerPos(at: curDepth, range: scannerRange)
                if (scannerPos == 0) {
                    print("Tripped scanner at \(curDepth)")
                    severity += curDepth * scannerRange
                }
            }
        }
        
        print("Trip severity: \(severity)")
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
