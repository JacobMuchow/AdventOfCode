//
//  Day12Pt1.swift
//  Advent
//
//  Created by Jacob Muchow on 11/29/24.
//

import Foundation

class Day12Pt1 {
    class Program {
        let id: String
        var pipes: [String] = []
        
        init(id: String) {
            self.id = id
        }
    }
    
    static func run() {
        let lines = IOUtils.readLinesFromFile("day12_input.txt")
        
        let programsMap = parsePrograms(from: lines)
        
        let startId = "0"
        let count = countPrograms(reachableFrom: startId, programsMap: programsMap)
        print("\(count) reachable programs from program '\(startId)'")
    }
    
    static func countPrograms(reachableFrom startId: String, programsMap: [String: Program]) -> Int {
        var count = 0
        var visited: Set<String> = []
        var queue: [String] = [startId]
        
        while !queue.isEmpty {
            let currentId = queue.removeFirst()
            if visited.contains(currentId) { continue }
            
            visited.insert(currentId)
            count += 1
            
            for pipe in programsMap[currentId]!.pipes {
                queue.append(pipe)
            }
        }
        
        return count
    }
    
    static func parsePrograms(from lines: [String]) -> [String:Program] {
        var programsMap: [String:Program] = [:]
        
        for line in lines {
            let tokens = line.split(separator: " <-> ")
            let programId = String(tokens[0])
            let pipes = tokens[1].split(separator: ",").map({ String($0) }).map({ $0.trimmingCharacters(in: .whitespaces) })
            
            let program = Program(id: programId)
            program.pipes = pipes
            programsMap[programId] = program
        }
        
        return programsMap
    }
}
