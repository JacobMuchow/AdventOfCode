//
//  main.swift
//  Advent
//
//  Created by Jacob Muchow on 9/3/24.
//

import Foundation

let currentDir = URL(fileURLWithPath: FileManager.default.currentDirectoryPath)
let fileURL = currentDir.appendingPathComponent("input.txt")

let lines: [String]

do {
    let content = try! String(contentsOf: fileURL, encoding: .utf8)
    lines = content.components(separatedBy: .newlines)
}

let sequence = lines[0]
var total = 0

var indexA = sequence.startIndex

while indexA != sequence.endIndex {
    var indexB = sequence.index(after: indexA)
    if indexB == sequence.endIndex {
        indexB = sequence.startIndex
    }

    if sequence[indexA] == sequence[indexB] {
        let val = sequence[indexA]
        let numVal = Int("\(val)", radix: 10)!

        total += numVal
    }

    indexA = sequence.index(after: indexA)
}

print("Total: \(total)")
