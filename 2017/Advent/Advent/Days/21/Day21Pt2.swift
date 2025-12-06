//
//  Day21Pt2.swift
//  Advent
//
//  Created by Jacob Muchow on 12/5/25.
//

class Day21Pt2 {
    static func run() {
        let lines = IOUtils.readLinesFromFile("day21_input.txt")
        
        // Create rule map. All possible permutations of rotating/flipping the input are cached in the map.
        var ruleMap: [String: [[Character]]] = [:]
        for line in lines {
            let parts = line.split(separator: " => ")
            let rule = String(parts[0])
            let output = String(parts[1])
            
            for perm in allRulePermutations(rule: rule) {
                ruleMap[perm] = decodeGrid(output)
            }
        }
        
        let start = ".#./..#/###"
        var grid = decodeGrid(start)
        
        for _ in 0..<18 {
            grid = expand(grid: grid, ruleMap: ruleMap)
        }
        
        var onCount = 0
        for y in 0..<grid.count {
            for x in 0..<grid.count {
                if grid[y][x] == "#" {
                    onCount += 1
                }
            }
        }
        
        print("On count: \(onCount)")
    }
    
    private static func expand(grid: [[Character]], ruleMap: [String: [[Character]]]) -> [[Character]] {
        let isEven = grid.count % 2 == 0
        let expandedSize = isEven ? grid.count / 2 * 3 : grid.count / 3 * 4
        let oldRangeSize = isEven ? 2 : 3
        let newRangeSize = isEven ? 3 : 4
        
        var expanded: [[Character]] = Array(repeating: Array(repeating: " ", count: expandedSize), count: expandedSize)
        
        var yOld = 0, xOld = 0, yNew = 0, xNew = 0
        
        while yOld < grid.count {
            xOld = 0
            xNew = 0
            
            while xOld < grid.count {
                let subAreaStr = encodeRange(grid, x: xOld, y: yOld, size: oldRangeSize)
                guard let newAreaGrid = ruleMap[subAreaStr] else {
                    fatalError("Rule not found in map: " + subAreaStr)
                }
                
                for j in 0..<newRangeSize {
                    for i in 0..<newRangeSize {
                        expanded[yNew+j][xNew+i] = newAreaGrid[j][i]
                    }
                }
                
                xOld += oldRangeSize
                xNew += newRangeSize
            }
            
            yOld += oldRangeSize
            yNew += newRangeSize
        }
        
        return expanded
    }
    
    private static func allRulePermutations(rule: String) -> [String] {
        var grid = decodeGrid(rule)
        var permutations = [grid]
        
        // Rotate 90deg 3x
        grid = rotate90(grid: grid)
        permutations.append(grid)
        grid = rotate90(grid: grid)
        permutations.append(grid)
        grid = rotate90(grid: grid)
        permutations.append(grid)
        
        // Flip
        grid = flipVertical(grid: grid)
        permutations.append(grid)
        
        // Rotate 3x again
        grid = rotate90(grid: grid)
        permutations.append(grid)
        grid = rotate90(grid: grid)
        permutations.append(grid)
        grid = rotate90(grid: grid)
        permutations.append(grid)

        
        return permutations.map { encodeGrid($0) }
    }
    
    private static func rotate90(grid: [[Character]]) -> [[Character]] {
        var out = Array(grid)
        for y in 0..<grid.count {
            for x in 0..<grid.count {
                out[y][x] = grid[grid.count-1-x][y]
            }
        }
        return out
    }
    
    private static func flipVertical(grid: [[Character]]) -> [[Character]] {
        var out = Array(grid)
        for y in 0..<grid.count {
            for x in 0..<grid.count {
                out[y][x] = grid[grid.count-1-y][x]
            }
        }
        return out
    }
    
    private static func decodeGrid(_ encoded: String) -> [[Character]] {
        let rows = encoded.split(separator: "/")
        return rows.map { Array($0) }
    }
    
    private static func encodeGrid(_ grid: [[Character]]) -> String {
        return grid.map { String($0) }.joined(separator: "/")
    }
    
    private static func encodeRange(_ grid: [[Character]], x: Int, y: Int, size: Int) -> String {
        var subArea: [[Character]] = []
        for j in y..<y+size {
            var row: [Character] = []
            for i in x..<x+size {
                row.append(grid[j][i])
            }
            subArea.append(row)
        }
        return encodeGrid(subArea)
    }
    
    private static func printGrid(_ grid: [[Character]]) {
        for row in grid {
            print(String(row))
        }
    }
}
