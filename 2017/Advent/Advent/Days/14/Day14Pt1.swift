//
//  Day14Pt1.swift
//  Advent
//
//  Created by Jacob Muchow on 11/29/24.
//

import Foundation

class Day14Pt1 {
    static func run() {
        let lines = IOUtils.readLinesFromFile("day14_input.txt")
        let input = lines[0]
        
        var count = 0

        for i in 0..<128 {
            let hashInput = "\(input)-\(i)"
            let hash = KnotHash.hash(hashInput)
            let bitstr = hexToBitStr(hash)
            
            bitstr.forEach({
                if $0 == "1" { count += 1 }
            })
        }
        
        print("Count: \(count)")
    }
    
    static func hexToBitStr(_ hex: String) -> String {
        // This creates a list where each car is converted to a String of 1s and 0s (unpadded).
        let bitArray = hex
            .map { Int(String($0), radix: 16)! }
            .map { String($0, radix: 2) }
        
        // This pads out each character to length 4.
        let paddedArray = bitArray.map({
            let paddingCount = max(0, 4 - $0.count)
            if paddingCount == 0 { return $0 }
            
            let padding = String(repeating: "0", count: paddingCount)
            return padding + $0
        })
        
        return paddedArray.joined()
    }
}
