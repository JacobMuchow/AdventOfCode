//
//  Day18Pt2.swift
//  Advent
//
//  Created by Jacob Muchow on 12/1/24.
//

import Foundation

class Day18Pt2 {
    static let isRegisterRegex = try! Regex("^[A-Za-z]")
    
    class Program {
        let id: Int
        var registers: [String:Int]
        var pos: Int = 0
        var exited = false
        
        init(id: Int) {
            self.id = id
            self.registers = ["p": id]
        }
    }
    
    static func run() {
        let lines = IOUtils.readLinesFromFile("day18_test.txt")
        
        let programs = [
            Program(id: 0),
            Program(id: 1)
        ]
        
        var curProgram = 0
        var lastSentFreq: Int? = nil
        
        while !programs[0].exited || !programs[1].exited {
            let program = programs[curProgram]
            
            let tokens = lines[program.pos].split(separator: " ")
            let cmd = tokens[0]
            
            switch cmd {
            case "set":
                let reg = String(tokens[1])
                let val = valueFor(input: String(tokens[2]), program: program)
                program.registers[reg] = val
                break
                
            case "add":
                let reg = String(tokens[1])
                let val = valueFor(input: String(tokens[2]), program: program)
                program.registers[reg] = program.registers[reg, default: 0] + val
                break
                
            case "mul":
                let reg = String(tokens[1])
                let val = valueFor(input: String(tokens[2]), program: program)
                program.registers[reg] = program.registers[reg, default: 0] * val
                break
                
            case "mod":
                let reg = String(tokens[1])
                let val = valueFor(input: String(tokens[2]), program: program)
                program.registers[reg] = program.registers[reg, default: 0] % val
                break
                
            case "jgz":
                let cond = valueFor(input: String(tokens[1]), program: program)
                if cond > 0 {
                    let jump = valueFor(input: String(tokens[2]), program: program)
                    program.pos += jump
                    continue
                }
                break
                
            case "snd":
                let val = valueFor(input: String(tokens[1]), program: program)
                lastSentFreq = val
                break
                
            case "rcv":
                let cond = valueFor(input: String(tokens[1]), program: program)
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
            
            program.pos += 1
        }
        
        print("Program exited.")
    }
    
    static func valueFor(input: String, program: Program) -> Int {
        if let _ = try! isRegisterRegex.prefixMatch(in: input) {
            return program.registers[input, default: 0]
        } else {
            return Int(input)!
        }
    }
}
