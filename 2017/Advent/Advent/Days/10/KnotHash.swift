//
//  KnotHash.swift
//  Advent
//
//  Created by Jacob Muchow on 11/30/24.
//

class KnotHash {
    static func hash(_ input: String) -> String {
        let transformedInput = transformInput(input)
        let sparseHash = hashSparse(lengths: transformedInput)
        return hashDense(sparseHash)
    }
    
    private static func transformInput(_ input: String) -> [Int] {
        var values = input.compactMap(\.asciiValue).map({ Int($0) })
        values.append(contentsOf: [17, 31, 73, 47, 23])
        return values
    }
    
    private static func hashSparse(lengths: [Int]) -> [Int] {
        var output = Array(0..<256)
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
    
    private static func hashDense(_ list: [Int]) -> String {
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
}
