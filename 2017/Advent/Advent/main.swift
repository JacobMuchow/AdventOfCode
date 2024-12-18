//
//  main.swift
//  Advent
//
//  Created by Jacob Muchow on 9/3/24.
//

import Foundation

func runSolution() {
    Day20Pt2.run()
}


print("Running solution...")
let start = Date()
runSolution()

let diff = start.distance(to: Date())
print("Solution ran in \(diff)")
