//
//  Day24Pt1.swift
//  Advent
//
//  Created by Jacob Muchow on 12/5/25.
//

class Day24Pt1 {
    static func run() {
        let lines = IOUtils.readLinesFromFile("day24_input.txt")
        
        var partPool: [Part] = []
        for i in 0..<lines.count {
            let tokens = lines[i].split(separator: "/")
            partPool.append(Part(
                id: i+1,
                port1: Int(String(tokens[0]))!,
                port2: Int(String(tokens[1]))!
            ))
        }
        
        var bridge = [Part(id: 0, port1: 0, port2: 0)]
        
        let maxStrength = tryParts(bridge: &bridge, partPool: &partPool)
        
        print("Max strength: \(maxStrength)")
    }
    
    private static func tryParts(bridge: inout [Part], partPool: inout [Part]) -> Int {
        var maxStrength = calcStrength(bridge: bridge)
        var pinMatch = openPortPins(bridge: bridge)
        
        // Try all parts forward.
        for (i, part) in partPool.enumerated() {
            if (part.port1 != pinMatch) { continue }
            
            partPool.remove(at: i)
            bridge.append(part)
            
            var strength = tryParts(bridge: &bridge, partPool: &partPool)
            maxStrength = max(maxStrength, strength)
            
            bridge.removeLast()
            partPool.insert(part, at: i)
        }
        
        // Try all parts backward.
        for (i, part) in partPool.enumerated() {
            if (part.port2 != pinMatch) { continue }
            
            partPool.remove(at: i)
            bridge.append(Part(id: part.id, port1: part.port2, port2: part.port1))
            
            var strength = tryParts(bridge: &bridge, partPool: &partPool)
            maxStrength = max(maxStrength, strength)
            
            bridge.removeLast()
            partPool.insert(part, at: i)
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
    
    struct Part {
        let id: Int
        let port1: Int
        let port2: Int
        
        init(id: Int, port1: Int, port2: Int) {
            self.id = id
            self.port1 = port1
            self.port2 = port2
        }
    }
    
    enum Dir {
        case Fwd;
        case Rev;
    }
}
