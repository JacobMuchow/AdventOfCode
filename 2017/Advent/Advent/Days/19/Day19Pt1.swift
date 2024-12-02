//
//  Day19Pt1.swift
//  Advent
//
//  Created by Jacob Muchow on 12/2/24.
//

import Foundation

class Day19Pt1 {
    typealias Grid = [[String]]
    
    enum Dir {
        case Up, Down, Right, Left
    }
    
    struct QueueItem {
        let pos: (Int, Int)
        let dir: Dir
    }
    
    static func run() {
        let lines = IOUtils.readLinesFromFile("day19_input.txt")
        
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
        var markers: [String] = []
        
        var queue: [QueueItem] = [
            QueueItem(pos: start, dir: Dir.Down)
        ]
        
        while !queue.isEmpty {
            let item = queue.removeFirst()
            let pos = item.pos;
            let dir = item.dir;
            let (x, y) = pos
            
            // Ignore invalid positions
            if x < 0 || x >= grid[0].count || y < 0 || y >= grid.count {
                continue
            }
            
            let val = grid[y][x]
            
            switch val {
            // Ignore import spaces.
            case " ":
                continue
                
            // Handle corners.
            case "+":
                if dir == Dir.Up || dir == Dir.Down {
                    queue.append(QueueItem(pos: (x+1, y), dir: Dir.Right))
                    queue.append(QueueItem(pos: (x-1, y), dir: Dir.Left))
                } else {
                    queue.append(QueueItem(pos: (x, y+1), dir: Dir.Down))
                    queue.append(QueueItem(pos: (x, y-1), dir: Dir.Up))
                }
                continue
                
            // Handle "|", "-" and any letter markers.
            default:
                if val != "|" && val != "-" {
                    markers.append(val)
                }
                
                if dir == Dir.Down {
                    queue.append(QueueItem(pos: (x, y+1), dir: Dir.Down))
                } else if dir == Dir.Up {
                    queue.append(QueueItem(pos: (x, y-1), dir: Dir.Up))
                } else if dir == Dir.Right {
                    queue.append(QueueItem(pos: (x+1, y), dir: Dir.Right))
                } else {
                    queue.append(QueueItem(pos: (x-1, y), dir: Dir.Left))
                }
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
