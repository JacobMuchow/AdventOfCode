//
//  Day15Pt2.swift
//  Advent
//
//  Created by Jacob Muchow on 11/30/24.
//

import Foundation

class Day15Pt2 {
    static func run() {
        let lines = IOUtils.readLinesFromFile("day15_test.txt")
        var valueA = UInt64(lines[0])!
        var valueB = UInt64(lines[1])!
        
        print("Gen A start: \(valueA)")
        print("Gen B start: \(valueB)")
        
        var matchCount = 0
        
        for i in 0..<40_000_000 {
            if i % 1_000_000 == 0 {
                print("Loop \(i)")
            }
            
            valueA = (valueA * 16807) % 2147483647
            valueB = (valueB * 48271) % 2147483647
            
            let bitsA = last16Bits(from: valueA)
            let bitsB = last16Bits(from: valueB)
            
            if (bitsA == bitsB) {
                matchCount += 1
            }
        }
        
        print("Match count: \(matchCount)")
    }
    
    static func last16Bits(from input: UInt64) -> String {
        let bits = String(input, radix: 2)
        if bits.count == 16 {
            return bits
        } else if bits.count > 16 {
            // Limit to last 16 chars
            return String(bits.suffix(16))
        } else {
            // Pad
            let padding = String(repeating: "0", count: 16 - bits.count)
            return padding + bits
        }
    }
}
