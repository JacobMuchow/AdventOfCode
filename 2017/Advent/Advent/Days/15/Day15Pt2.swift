//
//  Day15Pt2.swift
//  Advent
//
//  Created by Jacob Muchow on 11/30/24.
//

import Foundation

class Day15Pt2 {
    static func run() {
        let lines = IOUtils.readLinesFromFile("day15_input.txt")
        var valueA = UInt64(lines[0])!
        var valueB = UInt64(lines[1])!
        
        print("Gen A start: \(valueA)")
        print("Gen B start: \(valueB)")
        
        var matchCount = 0
        
        for i in 0..<5_000_000 {
            if i % 100_000 == 0 {
                print("Loop \(i)")
            }
            
            valueA = nextAcceptableValue(after: valueA, factor: 16807, divisor: 4)
            valueB = nextAcceptableValue(after: valueB, factor: 48271, divisor: 8)
            
            let bitsA = last16Bits(from: valueA)
            let bitsB = last16Bits(from: valueB)
            
            if (bitsA == bitsB) {
                matchCount += 1
            }
        }
        
        print("Match count: \(matchCount)")
    }
    
    static func nextAcceptableValue(after prevValue: UInt64, factor: UInt64, divisor: UInt64) -> UInt64 {
        var value = prevValue
        while true {
            value = (value * factor) % 2147483647
            if value % divisor == 0 { break }
        }
        
        return value
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
