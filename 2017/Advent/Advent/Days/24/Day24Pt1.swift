//
//  Day24Pt1.swift
//  Advent
//
//  Created by Jacob Muchow on 12/5/25.
//

class Day24Pt1 {
    static func run() {
        let lines = IOUtils.readLinesFromFile("day24_input.txt")
        
        var partPool: [Int: [Part]] = [:]
        for i in 0..<lines.count {
            let tokens = lines[i].split(separator: "/")
            
            let partFwd = Part(
                id: i+1,
                port1: Int(String(tokens[0]))!,
                port2: Int(String(tokens[1]))!
            )
            partPool[partFwd.port1, default: []].append(partFwd)
            
            let partRev = Part(
                id: i+1,
                port1: Int(String(tokens[1]))!,
                port2: Int(String(tokens[0]))!
            )
            partPool[partRev.port1, default: []].append(partRev)
        }
        
        var bridge = Bridge()
        var usedParts = Set<Int>()
        
        let maxStrength = tryParts(bridge: &bridge, partPool: &partPool, usedParts: &usedParts)
        
        print("Max strength: \(maxStrength)")
    }
    
    private static func tryParts(bridge: inout Bridge, partPool: inout [Int: [Part]], usedParts: inout Set<Int>) -> Int {
        var maxStrength = bridge.strength
        let pinMatch = bridge.parts.last!.port2
        
        let possibleParts = partPool[pinMatch, default: []]
        
        for part in possibleParts {
            if usedParts.contains(part.id) { continue }
            
            bridge.addPart(part)
            usedParts.insert(part.id)
            
            let strength = tryParts(bridge: &bridge, partPool: &partPool, usedParts: &usedParts)
            maxStrength = max(maxStrength, strength)
            
            bridge.popLastPart()
            usedParts.remove(part.id)
        }
 
        return maxStrength
    }
    
    class Bridge {
        var parts: [Part] = [Part(id: 0, port1: 0, port2: 0)]
        var strength: Int = 0
        
        func openPinCount() -> Int {
            return parts.last!.port2
        }
        
        func addPart(_ part: Part) {
            self.parts.append(part)
            self.strength += part.port1 + part.port2
        }
        
        func popLastPart()  {
            let part = self.parts.popLast()!
            self.strength -= part.port1 + part.port2
        }
    }
    
    struct Part: CustomStringConvertible {
        let id: Int
        let port1: Int
        let port2: Int
        
        init(id: Int, port1: Int, port2: Int) {
            self.id = id
            self.port1 = port1
            self.port2 = port2
        }
        
        var description: String {
            "\(self.id)|\(self.port1)/\(self.port2)"
        }
    }
}
