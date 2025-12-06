//
//  Day21Pt1.swift
//  Advent
//
//  Created by Jacob Muchow on 12/5/25.
//

class Day23Pt1 {
    static var registers: [String:Int] = [:]
    static let isRegisterRegex = try! Regex("^[A-Za-z]")
    
    static func run() {
        let lines = IOUtils.readLinesFromFile("day23_input.txt")
        
        var pos = 0
        var mulCount = 0
        
        while pos >= 0 && pos < lines.count {
            let tokens = lines[pos].split(separator: " ")
            let cmd = tokens[0]
            
            switch cmd {
            case "set":
                let reg = String(tokens[1])
                let val = valueFor(input: String(tokens[2]))
                registers[reg] = val
                break
                
            case "sub":
                let reg = String(tokens[1])
                let val = valueFor(input: String(tokens[2]))
                registers[reg] = registers[reg, default: 0] - val
                break
                
            case "mul":
                mulCount += 1
                let reg = String(tokens[1])
                let val = valueFor(input: String(tokens[2]))
                registers[reg] = registers[reg, default: 0] * val
                break
            
            case "jnz":
                let valX = valueFor(input: String(tokens[1]))
                if (valX != 0) {
                    let valY = valueFor(input: String(tokens[2]))
                    pos += valY
                    continue
                }
                
            default:
                fatalError("Unknown command: \(cmd)")
            }
            
            pos += 1
        }
        
        print("Program exited.")
        print("Mul count: \(mulCount)")
    }
    
    static func valueFor(input: String) -> Int {
        if let _ = try! isRegisterRegex.prefixMatch(in: input) {
            return registers[input, default: 0]
        } else {
            return Int(input)!
        }
    }
}
