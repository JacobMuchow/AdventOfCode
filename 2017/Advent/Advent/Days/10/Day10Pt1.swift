//
//  Day10Pt1.swift
//  Advent
//
//  Created by Jacob Muchow on 11/29/24.
//

import Foundation

class Day10Pt1 {
    static func run() {
        let lines = IOUtils.readLinesFromFile("day10_test.txt")
        let listSize = Int(lines[0])!
        let inputs = lines[1].split(separator: ",").map({ Int($0)! })
        
        let list = Array(0..<listSize)
        print("List: \(list)")
        
        print("Inputs: \(inputs)")
    }
}
