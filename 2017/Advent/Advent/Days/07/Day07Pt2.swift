//
//  Day07Pt2.swift
//  Advent
//
//  Created by Jacob Muchow on 11/28/24.
//

import Foundation

class Day07Pt2 {
    class Disc {
        let name: String
        var weight: Int = 0
        var stackWeight: Int = 0
        var parent: String?
        var children: [String] = []
        
        init(name: String) {
            self.name = name
        }
    }
    
    static func run() {
        let lines = IOUtils.readLinesFromFile("day07_input.txt")
        let discMap = parseDiscs(lines)
        
        // Find root disc.
        let rootDisc = discMap.values.first(where: { $0.parent == nil })!
        print("Root disc: \(rootDisc.name)")
        
        // Calculate the "stack" weights of each disc.
        calcWeights(discMap, disc: rootDisc)
        
        // Determine which weight value is the unbalanced one, and which is balanced (or will be...)
        var weightCounts: [Int: Int] = [:]
        for child in rootDisc.children {
            let childDisc = discMap[child]!
            weightCounts[childDisc.stackWeight, default: 0] += 1
        }
        
        // Find what the weight diff needs to be to balance the tower.
        let unbalancedWeight = weightCounts.first(where: { $0.value == 1 })!.key
        let balancedWeight = weightCounts.first(where: { $0.value > 1 })!.key
        let balanceDiff = balancedWeight - unbalancedWeight
        
        print("Balanced weight: \(balancedWeight)")
        print("Unbalanced weight: \(unbalancedWeight)")
        print("Diff: \(balanceDiff)")
        
        // Search within the tree to find the specific disc we want to rebalance so the whole tree is balanced.
        let unbalancedDisc = findUnbalancedDisc(discMap, rootDisc: rootDisc)
        print("Unbalanced disc: \(unbalancedDisc.name)")
        print("New weight: \(unbalancedDisc.weight + balanceDiff)")
    }
    
    static func findUnbalancedDisc(_ discMap: [String: Disc], rootDisc: Disc) -> Disc {
        // No further downward we can look, this is the disc that needs to change weights.
        if rootDisc.children.isEmpty {
            return rootDisc
        }
        
        var weightCounts: [Int: Int] = [:]
        for child in rootDisc.children {
            let childDisc = discMap[child]!
            weightCounts[childDisc.stackWeight, default: 0] += 1
        }
        
        // If there is only 1 weight in the dict, then the children are balanced,
        // so the current disc is the one we want.
        if weightCounts.count == 1 {
            return rootDisc
        }
        
        // Find what the weight diff needs to be to balance the tower.
        let unbalancedWeight = weightCounts.first(where: { $0.value == 1 })!.key
        let unbalancedDisc = discMap.first(where: { $0.value.stackWeight == unbalancedWeight })!.value
        
        // Recursively search through this disc.
        return findUnbalancedDisc(discMap, rootDisc: unbalancedDisc)
    }
    
    static func calcWeights(_ discMap: [String: Disc], disc: Disc) -> Void {
        var stackWeight = disc.weight
        
        // Add stack weights of children to the total.
        for child in disc.children {
            let childDisc = discMap[child]!
            // Recursively calculate the stack weight of each child as needed.
            if childDisc.stackWeight == 0 {
                calcWeights(discMap, disc: childDisc)
            }
            stackWeight += childDisc.stackWeight
        }
        
        disc.stackWeight = stackWeight
    }
    
    static func parseDiscs(_ lines: [String]) -> [String: Disc] {
        var discMap: [String: Disc] = [:]
        
        for line in lines {
            let parts = line.split(separator: "->")
            
            // Parse name & weight
            let leftMatch = parts[0].firstMatch(of: /([A-Za-z]+) \(([0-9]+)\)/)!
            let name = String(leftMatch.output.1)
            let weight = Int(leftMatch.output.2, radix: 10)!
            
            let disc = discMap[name] ?? Disc(name: name)
            disc.weight = weight
            
            // Parse children
            if (parts.count > 1) {
                parts[1].matches(of: /([A-Za-z]+)/).forEach {
                    let childName = String($0.output.1)
                    
                    disc.children.append(childName)
                    let childDisc = discMap[childName] ?? Disc(name: childName)
                    if (childDisc.parent != nil) {
                        fatalError("\(childName) already has a parent (\(childDisc.parent!))")
                    }
                    childDisc.parent = name
                    discMap[childName] = childDisc
                }
            }
            
            discMap[name] = disc
        }
        
        return discMap
    }
}
