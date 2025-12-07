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
        
        var bridge = [Part(id: 0, port1: 0, port2: 0)]
        var usedParts = Set<Int>()
        
        let maxStrength = tryParts(bridge: &bridge, partPool: &partPool, usedParts: &usedParts)
        
        print("Max strength: \(maxStrength)")
    }
    
    private static func tryParts(bridge: inout [Part], partPool: inout [Int: [Part]], usedParts: inout Set<Int>) -> Int {
        var maxStrength = calcStrength(bridge: bridge)
        let pinMatch = openPortPins(bridge: bridge)
        
        let possibleParts = partPool[pinMatch, default: []]
        
        for part in possibleParts {
            if usedParts.contains(part.id) { continue }
            
            bridge.append(part)
            usedParts.insert(part.id)
            
            let strength = tryParts(bridge: &bridge, partPool: &partPool, usedParts: &usedParts)
            maxStrength = max(maxStrength, strength)
            
            bridge.removeLast()
            usedParts.remove(part.id)
        }
 
        return maxStrength
    }
    
    private static func openPortPins(bridge: [Part]) -> Int {
        return bridge.last!.port2;
    }
    
    private static func calcStrength(bridge: [Part]) -> Int {
        return bridge.reduce(0, { acc, part in
            return acc + part.port1 + part.port2
        })
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
    
    enum Dir {
        case Fwd;
        case Rev;
    }
}
