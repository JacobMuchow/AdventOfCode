//
//  Day21Pt1.swift
//  Advent
//
//  Created by Jacob Muchow on 12/5/25.
//

class Day22Pt1 {
    static func run() {
        let lines = IOUtils.readLinesFromFile("day22_input.txt")
        let grid: [[Character]] = lines.map { Array($0) }
        
        let nodeGrid = NodeGrid(inputGrid: grid)
        
        let carrier = Carrier(
            x: (grid[0].count / 2),
            y: grid.count / 2,
            dir: Dir.U
        )
        
        var infectedCount = 0
        for _ in 0..<10000 {
            let infected = burst(carrier: carrier, nodeGrid: nodeGrid)
            if (infected) {
                infectedCount += 1
            }
        }
        
        print("Infected count: \(infectedCount)")
    }
    
    private static func burst(carrier: Carrier, nodeGrid: NodeGrid) -> Bool {
        let node = nodeGrid.getOrAddNode(x: carrier.x, y: carrier.y)
        
        if node.infected {
            carrier.dir = carrier.dir.turningRight()
        } else {
            carrier.dir = carrier.dir.turningLeft()
        }
        
        node.infected = !node.infected
        
        switch carrier.dir {
        case Dir.U: carrier.y -= 1; break;
        case Dir.D: carrier.y += 1; break;
        case Dir.R: carrier.x += 1; break;
        case Dir.L: carrier.x -= 1; break;
        }
        
        return node.infected
    }
    
    private class Carrier {
        var x: Int
        var y: Int
        var dir: Dir
        
        init(x: Int, y: Int, dir: Dir) {
            self.x = x
            self.y = y
            self.dir = dir
        }
    }
    
    private class NodeGrid {
        var nodes: [String: Node]
        
        init(inputGrid: [[Character]]) {
            self.nodes = [:]
            for y in 0..<inputGrid.count {
                for x in 0..<inputGrid[y].count {
                    let value = inputGrid[y][x]
                    let node = Node(infected: value == "#")
                    self.nodes[posKey(x, y)] = node
                }
            }
        }
        
        func getOrAddNode(x: Int, y: Int) -> Node {
            let key = posKey(x, y)
            if let node = nodes[posKey(x, y)] {
                return node
            }
            let node = Node(infected: false)
            self.nodes[key] = node
            return node
        }
        
        private func posKey(_ x: Int, _ y: Int) -> String {
            return "\(x),\(y)"
        }
    }
    
    private enum Dir {
        case U;
        case R;
        case D;
        case L;
        
        func turningRight() -> Dir {
            switch self {
            case Dir.U: return Dir.R;
            case Dir.R: return Dir.D;
            case Dir.D: return Dir.L;
            case Dir.L: return Dir.U;
            }
        }
        
        func turningLeft() -> Dir {
            switch self {
            case Dir.U: return Dir.L;
            case Dir.L: return Dir.D;
            case Dir.D: return Dir.R;
            case Dir.R: return Dir.U;
            }
        }
    }
    
    private class Node {
        var infected: Bool
        
        init(infected: Bool) {
            self.infected = infected
        }
    }
}

