//
//  Day18Pt1.swift
//  Advent
//
//  Created by Jacob Muchow on 12/1/24.
//

import Foundation

class Day18Pt1 {
    static var registers: [String:Int] = [:]
    static let isRegisterRegex = try! Regex("^[A-Za-z]")
    
    static func run() {
        let lines = IOUtils.readLinesFromFile("day18_input.txt")
        
        var pos = 0
        var lastSentFreq: Int? = nil
        
        while pos >= 0 && pos < lines.count {
            let tokens = lines[pos].split(separator: " ")
            let cmd = tokens[0]
            
            switch cmd {
            case "set":
                let reg = String(tokens[1])
                let val = valueFor(input: String(tokens[2]))
                registers[reg] = val
                break
                
            case "add":
                let reg = String(tokens[1])
                let val = valueFor(input: String(tokens[2]))
                registers[reg] = registers[reg, default: 0] + val
                break
                
            case "mul":
                let reg = String(tokens[1])
                let val = valueFor(input: String(tokens[2]))
                registers[reg] = registers[reg, default: 0] * val
                break
                
            case "mod":
                let reg = String(tokens[1])
                let val = valueFor(input: String(tokens[2]))
                registers[reg] = registers[reg, default: 0] % val
                break
                
            case "jgz":
                let cond = valueFor(input: String(tokens[1]))
                if cond > 0 {
                    let jump = valueFor(input: String(tokens[2]))
                    pos += jump
                    continue
                }
                break
                
            case "snd":
                let val = valueFor(input: String(tokens[1]))
                lastSentFreq = val
                break
                
            case "rcv":
                let cond = valueFor(input: String(tokens[1]))
                if cond > 0 {
                    if let freq = lastSentFreq {
                        print("Last received frequency: \(freq)")
                    } else {
                        fatalError("rcv command given, but no frequency has been sent.")
                    }
                    
                    // Exit program.
                    return
                }
                
            default:
                fatalError("Unknown command: \(cmd)")
            }
            
            pos += 1
        }
        
        print("Program exited.")
    }
    
    static func valueFor(input: String) -> Int {
        if let _ = try! isRegisterRegex.prefixMatch(in: input) {
            return registers[input, default: 0]
        } else {
            return Int(input)!
        }
    }
}
