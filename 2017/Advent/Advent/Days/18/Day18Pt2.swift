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
        var awaitingSignal = false
        var signalQueue: [Int] = []
        var sendCount: Int = 0
        
        init(id: Int) {
            self.id = id
            self.registers = ["p": id]
        }
    }
    
    static func run() {
        let lines = IOUtils.readLinesFromFile("day18_input.txt")
        
        let programs = [
            Program(id: 0),
            Program(id: 1)
        ]
        
        var curProgram = 0
        
        while true {
            let program = programs[curProgram]
            let otherProgram = programs[(curProgram+1) % programs.count]
            
            // Deadlock conditions
            if program.awaitingSignal && program.signalQueue.isEmpty &&
                otherProgram.awaitingSignal && otherProgram.signalQueue.isEmpty {
                print("Programs deadlocked. Both awaiting signals.")
                break
            }
            
            if (program.exited && otherProgram.awaitingSignal && otherProgram.signalQueue.isEmpty) {
                print("Program \(otherProgram.id) deadlocked. Awaiting signal while other program has exited.")
                break
            }
            
            if (otherProgram.exited && program.awaitingSignal && program.signalQueue.isEmpty) {
                print("Program \(otherProgram.id) deadlocked. Awaiting signal while other program has exited.")
                break
            }
            
            // Handle both programs existed
            if (program.exited && otherProgram.exited) {
                print("Both programs exited.")
                break
            }
            
            // Handle program "exited" by position
            if (program.pos < 0 || program.pos >= lines.count) {
                if !program.exited {
                    print("Program \(curProgram) exited.")
                    program.exited = true
                }
                curProgram = (curProgram+1) % programs.count
                break
            }
            
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
                otherProgram.signalQueue.append(val)
                program.sendCount += 1
                break
                
            case "rcv":
                let reg = String(tokens[1])
                if program.signalQueue.isEmpty {
                    program.awaitingSignal = true
                    
                    // Switch programs while waiting
                    curProgram = (curProgram+1) % programs.count
                    continue
                    
                } else {
                    program.awaitingSignal = false
                    let signal = program.signalQueue.removeFirst()
                    program.registers[reg] = signal
                }
                
            default:
                fatalError("Unknown command: \(cmd)")
            }
            
            program.pos += 1
        }
        
        print("Programs exited.")
        print("Program 1 send count: \(programs[1].sendCount)")
    }
    
    static func valueFor(input: String, program: Program) -> Int {
        if let _ = try! isRegisterRegex.prefixMatch(in: input) {
            return program.registers[input, default: 0]
        } else {
            return Int(input)!
        }
    }
}
