//
//  Day16Pt2.swift
//  Advent
//
//  Created by Jacob Muchow on 11/30/24.
//

import Foundation

class Day16Pt2 {
    static func run() {
        let lines = IOUtils.readLinesFromFile("day16_input.txt")
        var programs: [String] = lines[0].map { String($0) }
        let instructions = lines[1].split(separator: ",").map { String($0) }
        
        print("Order start: \(programs)")
        
        let startSpots = Array(programs)
        var cycleLength = 0
        
        while true {
            programs = dance(programs, instructions)
            cycleLength += 1
            
            if programs == startSpots { break }
        }
        
        let cyclesRemaining = 1_000_000_000 % cycleLength

        for _ in 0..<cyclesRemaining {
            programs = dance(programs, instructions)
        }
        
        print("Order end: \(programs)")
        print("Joined: \(programs.joined())")
    }
    
    static func dance(_ programs: [String], _ instructions: [String]) -> [String] {
        var output = programs
        
        for ins in instructions {
            let cmd = ins.prefix(upTo: ins.index(after: ins.startIndex))
            let args = ins.suffix(from: ins.index(after: ins.startIndex))
            
            if (cmd == "s") {
                let count = Int(args, radix: 10)!
                output = shift(output, count)
            } else if cmd == "x" {
                let tokens = args.split(separator: "/").map { Int($0)! }
                output = swap(output, tokens[0], tokens[1])
            } else if cmd == "p" {
                let tokens = args.split(separator: "/").map { String($0) }
                output = swap(output, tokens[0], tokens[1])
            } else {
                fatalError("Unknown instruction: \(cmd)")
            }
        }
        
        return output
    }
    
    static func shift(_ programs: [String], _ count: Int) -> [String] {
        let splitIndex = programs.count - count
        let left = programs[0..<splitIndex]
        let right = programs[splitIndex...]
        return Array(right + left)
    }
    
    static func swap(_ programs: [String], _ programA: String, _ programB: String) -> [String] {
        let indexA = programs.firstIndex(of: programA)!
        let indexB = programs.firstIndex(of: programB)!
        return swap(programs, indexA, indexB)
    }
    
    static func swap(_ programs: [String], _ indexA: Int, _ indexB: Int) -> [String] {
        var output = programs
        
        let swap = output[indexA]
        output[indexA] = output[indexB]
        output[indexB] = swap
        return output
    }
}
