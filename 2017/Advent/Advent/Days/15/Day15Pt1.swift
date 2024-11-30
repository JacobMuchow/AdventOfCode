//
//  Day15Pt1.swift
//  Advent
//
//  Created by Jacob Muchow on 11/30/24.
//

import Foundation

class Day15Pt1 {
    static func run() {
        let lines = IOUtils.readLinesFromFile("day15_test.txt")
        let startValueA = Int(lines[0])!
        let startValueB = Int(lines[1])!
        
        print("Gen A start: \(startValueA)")
        print("Gen B start: \(startValueB)")
    }
}
