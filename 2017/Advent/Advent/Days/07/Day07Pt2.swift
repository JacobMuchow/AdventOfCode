//
//  Day07Pt2.swift
//  Advent
//
//  Created by Jacob Muchow on 11/28/24.
//

import Foundation

class Day07Pt2 {
    struct Disc {
        let name: String
        var weight: Int = 0
        var parent: String?
        var children: [String] = []
    }
    
    static func run() {
        let lines = IOUtils.readLinesFromFile("day07_test.txt")

        var discMap: [String: Disc] = [:]
        
        for line in lines {
            let parts = line.split(separator: "->")
            
            // Parse name & weight
            let leftMatch = parts[0].firstMatch(of: /([A-Za-z]+) \(([0-9]+)\)/)!
            let name = String(leftMatch.output.1)
            let weight = Int(leftMatch.output.2, radix: 10)!
            
            var disc = discMap[name] ?? Disc(name: name)
            disc.weight = weight
            
            // Parse children
            if (parts.count > 1) {
                parts[1].matches(of: /([A-Za-z]+)/).forEach {
                    let childName = String($0.output.1)
                    
                    disc.children.append(childName)
                    var childDisc = discMap[childName] ?? Disc(name: childName)
                    if (childDisc.parent != nil) {
                        fatalError("\(childName) already has a parent (\(childDisc.parent!))")
                    }
                    childDisc.parent = name
                    discMap[childName] = childDisc
                }
            }
            
            discMap[name] = disc
        }
        
        // Find root disc
        let rootDisc = discMap.values.first(where: { $0.parent == nil })!
        print("Root disc: \(rootDisc.name)")
    }
}
