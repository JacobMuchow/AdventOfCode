//
//  Day14Pt2.swift
//  Advent
//
//  Created by Jacob Muchow on 11/30/24.
//

import Foundation

class Day14Pt2 {
    static func run() {
        let lines = IOUtils.readLinesFromFile("day14_test.txt")
        let input = lines[0]
        
        let grid = parseGrid(input)
        
        var count = 0
        for i in 0..<128 {
            for j in 0..<128 {
                if grid[i][j] == "#" {
                    count += 1
                }
            }
        }
        
        print("Count: \(count)")
    }
    
    static func parseGrid(_ input: String) -> [[String]] {
        // 128x128 grid, empty (".")
        var grid = Array(repeating: Array(repeating: ".", count: 128), count: 128)

        for i in 0..<128 {
            let hashInput = "\(input)-\(i)"
            let hash = KnotHash.hash(hashInput)
            let bitStr = hexToBitStr(hash)
            
            for j in 0..<128 {
                let idx = bitStr.index(bitStr.startIndex, offsetBy: j)
                
                if bitStr[idx] == "1" {
                    grid[i][j] = "#"
                }
            }
        }
        
        return grid
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
