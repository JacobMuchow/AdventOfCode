//
//  Day19Pt1.swift
//  Advent
//
//  Created by Jacob Muchow on 12/2/24.
//

import Foundation

class Day19Pt1 {
    typealias Grid = [[String]]
    
    struct QueueItem {
        let pos: (Int, Int)
        let lastPos: (Int, Int)
        let lastVal: String
    }
    
    static func run() {
        let lines = IOUtils.readLinesFromFile("day19_test.txt")
        
        let grid = parseGrid(lines: lines)
        for row in grid {
            print(row)
        }
        
        let start = findStart(grid: grid)
        print("Start pos: \(start)")
        
        let markers = findPathMarkers(grid: grid, start: start)
        print("Markers visited: \(markers.joined())")
    }
    
    static func findPathMarkers(grid: Grid, start: (Int, Int)) -> [String] {
        var visited: Set<String> = []
        var markers: [String] = []
        var queue: [QueueItem] = [
            QueueItem(pos: start, lastPos: start, lastVal: "|")
        ]
        
        while !queue.isEmpty {
            let item = queue.removeFirst()
            let pos = item.pos;
            let lastPos = item.lastPos;
            let lastval = item.lastVal;
            let (x, y) = pos
            
            // Ignore invalid positions
            if x < 0 || x >= grid[0].count || y < 0 || y >= grid.count {
                continue
            }
            
            // Do no re-visit positions
            let key = keyFor(pos: pos)
            if visited.contains(key) { continue }
            visited.insert(key)
            
            let val = grid[y][x]
            
            print("Pos: \(pos), val: \(val), last: \(lastval)")
            
            switch val {
            case " ":
                continue
                
            case "|":
                if lastval == "-" {
                    queue.append(QueueItem(pos: (x+1, y), lastPos: pos, lastVal: val))
                    queue.append(QueueItem(pos: (x-1, y), lastPos: pos, lastVal: val))
                } else {
                    queue.append(QueueItem(pos: (x, y+1), lastPos: pos, lastVal: val))
                    queue.append(QueueItem(pos: (x, y-1), lastPos: pos, lastVal: val))
                }
                continue
                
            case "-":
                if lastval == "|" {
                    queue.append(QueueItem(pos: (x, y+1), lastPos: pos, lastVal: val))
                    queue.append(QueueItem(pos: (x, y-1), lastPos: pos, lastVal: val))
                } else {
                    queue.append(QueueItem(pos: (x+1, y), lastPos: pos, lastVal: val))
                    queue.append(QueueItem(pos: (x-1, y), lastPos: pos, lastVal: val))
                }
                continue
                
            case "+":
                queue.append(QueueItem(pos: (x, y+1), lastPos: pos, lastVal: val))
                queue.append(QueueItem(pos: (x, y-1), lastPos: pos, lastVal: val))
                queue.append(QueueItem(pos: (x+1, y), lastPos: pos, lastVal: val))
                queue.append(QueueItem(pos: (x-1, y), lastPos: pos, lastVal: val))
                continue
                
            default:
                markers.append(val)
                queue.append(QueueItem(pos: (x, y+1), lastPos: pos, lastVal: val))
                queue.append(QueueItem(pos: (x, y-1), lastPos: pos, lastVal: val))
                queue.append(QueueItem(pos: (x+1, y), lastPos: pos, lastVal: val))
                queue.append(QueueItem(pos: (x-1, y), lastPos: pos, lastVal: val))
                continue
            }
        }
        
        return markers
    }
    
    static func findStart(grid: Grid) -> (Int, Int) {
        let firstRow = grid[0]
        for (i, val) in firstRow.enumerated() {
            if val == "|" {
                return (i, 0)
            }
        }
        fatalError("Couldn't find path start")
    }
    
    static func parseGrid(lines: [String]) -> Grid {
        var grid: [[String]] = []
        for line in lines {
            grid.append(line.map { String($0) })
        }
        return grid
    }
    
    static func keyFor(pos: (Int, Int)) -> String {
        return "\(pos.0),\(pos.1)"
    }
}
