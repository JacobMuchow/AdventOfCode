//
//  main.swift
//  Advent
//
//  Created by Jacob Muchow on 9/3/24.
//

import Foundation

print("Hello, World!")

//let currentDir = URL(fileURLWithPath: FileManager.default.currentDirectoryPath)
//
//print("Current dir: \(currentDir.absoluteString)")
//
//let fileURL = currentDir.appendingPathComponent("input.txt")
//
//print("File URL: \(fileURL)")
//
//do {
//    let content = try String(contentsOf: fileURL, encoding: .utf8)
//    print(content)
//} catch {
//    print("Error reading file: \(error.localizedDescription)")
//}
//
//


let sequence = "112345661"
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


//for i in 0..<sequence.count {
//    let j = i == sequence.count-1 ? 0 : i+1;
//
//    if sequence[i] == sequence[j] {
//        let val = Int(sequence[i], 10)
//    }
//}
