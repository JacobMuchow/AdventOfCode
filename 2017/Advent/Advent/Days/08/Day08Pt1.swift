//
//  Day08Pt1.swift
//  Advent
//
//  Created by Jacob Muchow on 11/28/24.
//

import Foundation

class Day08Pt1 {
    static func run() {
        let lines = IOUtils.readLinesFromFile("day08_input.txt")
        
        var registers: [String: Int] = [:]

        for line in lines {
            let tokens = line.split(separator: " ")
            let reg = String(tokens[0])
            let ins = String(tokens[1])
            let value = Int(tokens[2])!
            let condReg = String(tokens[4])
            let cond = String(tokens[5])
            let condValue = Int(tokens[6])!
            
            // Initialize register values. The names of the registers are not known at
            // compile time & are given through the list.
            if registers[reg] == nil {
                registers[reg] = 0
            }
            if registers[condReg] == nil {
                registers[condReg] = 0
            }
            
            // Evanluate the condition. If true, we will follow the instruction.
            let condRegValue = registers[condReg] ?? 0
            if !evalCondition(valA: condRegValue, cond: cond, valB: condValue) {
                continue;
            }
            
            // Execute the instruction.
            if (ins == "inc") {
                registers[reg]! += value;
            } else if (ins == "dec") {
                registers[reg]! -= value;
            } else {
                fatalError("Unknown instruction: \(ins)")
            }
        }
        
        // After execution, determine the large value in any register (the solution).
        let maxValue = registers.values.max()!
        print("Max value: \(maxValue)")
    }
    
    static func evalCondition(valA: Int, cond: String, valB: Int) -> Bool {
        if (cond == "==") {
            return valA == valB
        } else if (cond == "!=") {
            return valA != valB
        } else if (cond == ">") {
            return valA > valB
        } else if (cond == "<") {
            return valA < valB
        } else if (cond == ">=") {
            return valA >= valB
        } else if (cond == "<=") {
            return valA <= valB
        } else {
            fatalError("Unknown condition: \(cond)")
        }
    }
}
