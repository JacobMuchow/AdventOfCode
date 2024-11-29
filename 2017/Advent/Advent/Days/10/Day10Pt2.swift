//
//  Day10Pt2.swift
//  Advent
//
//  Created by Jacob Muchow on 11/29/24.
//

import Foundation

class Day10Pt2 {
    static func run() {
        let lines = IOUtils.readLinesFromFile("day10_input.txt")
        let listSize = Int(lines[0])!
        let list = Array(0..<listSize)
        
        var lengths = lines[1].compactMap(\.asciiValue).map({ Int($0) })
        lengths.append(contentsOf: [17, 31, 73, 47, 23])
        print("Lengths: \(lengths)")
        
        let sparseHash = hashSparse(list, lengths: lengths)
        let denseHash = hashDense(sparseHash)
        
        print("Hash: \(denseHash)")
    }
    
    static func hashDense(_ list: [Int]) -> String {
        var output = ""
        
        for i in 0..<16 {
            var denseVal = list[i*16]
            for j in 1..<16 {
                denseVal ^= list[i * 16 + j]
            }
            output.append(String(format: "%02x", denseVal))
        }
        
        return output
    }
    
    static func hashSparse(_ list: [Int], lengths: [Int]) -> [Int] {
        var output = list
        var curIdx = 0
        var skipSize = 0
        
        for _ in 0..<64 {
            for length in lengths {
                var i = curIdx
                var j = curIdx + length - 1
                
                while i < j {
                    let iSafe = i % output.count
                    let jSafe = j % output.count
                    
                    let swap = output[iSafe]
                    output[iSafe] = output[jSafe]
                    output[jSafe] = swap
                    
                    i += 1
                    j -= 1
                }
                
                curIdx = (curIdx + length + skipSize) % output.count
                skipSize += 1
            }
        }
        
        return output
    }
}
