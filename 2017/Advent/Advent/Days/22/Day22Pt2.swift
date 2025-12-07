//
//  Day22Pt2.swift
//  Advent
//
//  Created by Jacob Muchow on 12/5/25.
//

class Day22Pt2 {
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
        for _ in 0..<10000000 {
            let infected = burst(carrier: carrier, nodeGrid: nodeGrid)
            if (infected) {
                infectedCount += 1
            }
        }
        
        print("Infected count: \(infectedCount)")
    }
    
    private static func burst(carrier: Carrier, nodeGrid: NodeGrid) -> Bool {
        let node = nodeGrid.getOrAddNode(x: carrier.x, y: carrier.y)
        
        switch node.state {
        case NodeState.Clean:
            carrier.dir = carrier.dir.turningLeft()
            break
        case NodeState.Infected:
            carrier.dir = carrier.dir.turningRight()
            break
        case NodeState.Flagged:
            carrier.dir = carrier.dir.reversing()
            break
        case NodeState.Weakened:
            // Do nothing
            break
        }
        
        switch carrier.dir {
        case Dir.U: carrier.y -= 1; break;
        case Dir.D: carrier.y += 1; break;
        case Dir.R: carrier.x += 1; break;
        case Dir.L: carrier.x -= 1; break;
        }
        
        node.state = node.state.nextState()
        return node.state == NodeState.Infected
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
                    let node = Node(state: value == "#" ? NodeState.Infected : NodeState.Clean)
                    self.nodes[posKey(x, y)] = node
                }
            }
        }
        
        func getOrAddNode(x: Int, y: Int) -> Node {
            let key = posKey(x, y)
            if let node = nodes[posKey(x, y)] {
                return node
            }
            let node = Node(state: NodeState.Clean)
            self.nodes[key] = node
            return node
        }
        
        private func posKey(_ x: Int, _ y: Int) -> String {
            return "\(x),\(y)"
        }
    }
    
    private class Node {
        var state: NodeState
        
        init(state: NodeState) {
            self.state = state
        }
    }
    
    private enum NodeState {
        case Clean;
        case Weakened;
        case Infected;
        case Flagged;
        
        func nextState() -> NodeState {
            switch self {
            case NodeState.Clean: return NodeState.Weakened;
            case NodeState.Weakened: return NodeState.Infected;
            case NodeState.Infected: return NodeState.Flagged;
            case NodeState.Flagged: return NodeState.Clean;
            }
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
        
        func reversing() -> Dir {
            switch self {
            case Dir.U: return Dir.D;
            case Dir.D: return Dir.U;
            case Dir.L: return Dir.R;
            case Dir.R: return Dir.L;
            }
        }
    }
}
