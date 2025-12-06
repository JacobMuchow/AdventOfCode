//
//  main.swift
//  Advent
//
//  Created by Jacob Muchow on 9/3/24.
//

import Foundation

func runSolution() {
    Day22Pt2.run()
}


print("Running solution...")
let start = DispatchTime.now()
runSolution()

let end = DispatchTime.now()
let timeTakenNano = end.uptimeNanoseconds - start.uptimeNanoseconds
let timeTakenMs = Double(timeTakenNano) / 1_000_000.0
print(String(format: "Solution ran in %.3f ms", timeTakenMs))
