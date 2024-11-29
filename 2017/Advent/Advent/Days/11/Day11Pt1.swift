//
//  Day11Pt1.swift
//  Advent
//
//  Created by Jacob Muchow on 11/29/24.
//

import Foundation

class Day11Pt1 {
    static func run() {
        let lines = IOUtils.readLinesFromFile("day11_input.txt")
        let input = lines[0]
        
        let directions = input.split(separator: ",")
        print("Dirs: \(directions)")
        
        // We will think of this is an XY coordinate system.
        // Moving diagonally is +/- 1 X & Y depending on the direction.
        // Moving vertically is +/- 2 Y.
        
        // Determine the final coordinates by following all the directions.
        // From here we can work out what is the most optimal step count.
        var x = 0
        var y = 0
        
        for dir in directions {
            if dir == "n" {
                y += 2
            } else if dir == "s" {
                y -= 2
            } else if dir == "ne" {
                x += 1
                y += 1
            } else if dir == "se" {
                x += 1
                y -= 1
            } else if dir == "nw" {
                x -= 1
                y += 1
            } else if dir == "sw" {
                x -= 1
                y -= 1
            } else {
                fatalError("Uknown direction: \(dir)")
            }
        }
        
        print("Final coords: \(x), \(y)")
        
        // To decide most optimal step count, we will move horizontally steps,
        // counting X steps. We will subtracting this from Y. At this point we
        // should be in the same column as the ending coordinate. The steps left
        // should be directly N/S, we can divide by 2 and add to step count.
        var stepCount = 0
        stepCount += abs(x)
        
        let disLeft = abs(y) - abs(x)
        if !disLeft.isMultiple(of: 2) {
            fatalError("Invalid state, expected multiple of 2")
        }
        stepCount += disLeft / 2
        
        print("Step count: \(stepCount)")
    }
}
