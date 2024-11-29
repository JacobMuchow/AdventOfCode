//
//  Day12Pt2.swift
//  Advent
//
//  Created by Jacob Muchow on 11/29/24.
//

import Foundation

class Day12Pt2 {
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
        
        let groupCount = countGroups(in: programsMap)
        print("Group count: \(groupCount)")
    }
    
    static func countGroups(in programsMap: [String: Program]) -> Int {
        var groupCount = 0
        var programsLeft = Array(programsMap.keys)
        
        while !programsLeft.isEmpty {
            let startId = programsLeft.first!
            let group = findGroup(reachableFrom: startId, programsMap: programsMap)
            groupCount += 1
            
            // Remove each program in the group from the list.
            for programId in group {
                let idx = programsLeft.firstIndex(of: programId)!
                programsLeft.remove(at: idx)
            }
        }
        
        return groupCount
    }
    
    static func findGroup(reachableFrom startId: String, programsMap: [String: Program]) -> Set<String> {
        var visited: Set<String> = []
        var queue: [String] = [startId]
        
        while !queue.isEmpty {
            let currentId = queue.removeFirst()
            if visited.contains(currentId) { continue }
            
            visited.insert(currentId)
            
            for pipe in programsMap[currentId]!.pipes {
                queue.append(pipe)
            }
        }
        
        return visited
    }
    
    static func parsePrograms(from lines: [String]) -> [String:Program] {
        var programsMap: [String:Program] = [:]
        
        for line in lines {
            let tokens = line.split(separator: " <-> ")
            let programId = String(tokens[0])
            let pipes = tokens[1].split(separator: ",").map({ String($0) }).map({ $0.trimmingCharacters(in: .whitespaces) })
            
            var program = Program(id: programId)
            program.pipes = pipes
            programsMap[programId] = program
        }
        
        return programsMap
    }
}
