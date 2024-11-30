//
//  Day14Pt2.swift
//  Advent
//
//  Created by Jacob Muchow on 11/30/24.
//

import Foundation

class Day14Pt2 {
    static func run() {
        let lines = IOUtils.readLinesFromFile("day14_input.txt")
        let input = lines[0]
        
        let grid = parseGrid(input)
        let regionCount = countRegions(grid)
        
        print("Region count: \(regionCount)")
    }
    
    static func countRegions(_ grid: [[String]]) -> Int {
        var posToRegionMap: [String: Int] = [:]
        var regionCount: Int = 0
        
        for y in 0..<128 {
            for x in 0..<128 {
                if grid[y][x] == "." { continue }
                if posToRegionMap[keyFor(pos: (x, y))] == nil {
                    let region = discoverRegion(grid: grid, startPos: (x, y))
                    regionCount += 1
                    region.forEach { posToRegionMap[keyFor(pos: $0)] = regionCount }
                }
            }
        }
        
        return regionCount
    }
    
    // Given a starting pos, search for all connected neighbors and return a list of coords for the entire region.
    static func discoverRegion(grid: [[String]], startPos: (Int, Int)) -> [(Int, Int)] {
        var visited: Set<String> = []
        var region: [(Int, Int)] = [startPos]
        var queue: [(Int, Int)] = [startPos]
        
        while !queue.isEmpty {
            let (x, y) = queue.removeFirst()
            
            // Ignore invalid positions.
            if (x < 0 || y < 0 || x >= grid[0].count || y >= grid.count) {
                continue
            }
            
            // Skip already visited positions.
            let key = keyFor(pos: (x, y))
            if (visited.contains(key)) {
                continue
            }
            visited.insert(key)
            
            // Add pos to region, and enqueue neighbors.
            if grid[y][x] == "#" {
                region.append((x, y))
                queue.append((x+1, y))
                queue.append((x-1, y))
                queue.append((x, y+1))
                queue.append((x, y-1))
            }
        }
        
        return region
    }
    
    static func keyFor(pos: (Int, Int)) -> String {
        return "\(pos.0),\(pos.1)"
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
