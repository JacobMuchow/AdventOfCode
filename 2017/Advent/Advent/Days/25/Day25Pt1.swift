//
//  Day25Pt1.swift
//  Advent
//
//  Created by Jacob Muchow on 12/5/25.
//

class Day25Pt1 {
    static func run() {
        let lines = IOUtils.readLinesFromFile("day25_input.txt")
        let blueprint = parseBlueprint(from: lines)
        

        var curState = blueprint.startState
        var curNode = Node()
        let nodeList = NodeList(nodes: [curNode])
        
        for _ in 0..<blueprint.diagnosticStep {
            let action = blueprint.actionMap[mapKey(curState, curNode.value)]!
            
            curNode.value = action.writeValue
            curNode = nodeList.neighbor(of: curNode, dir: action.moveDir)
            curState = action.nextState
        }
        
        print("Checksum: \(nodeList.checksum())")
    }
    
    class NodeList {
        var nodes: [Node]
        
        init(nodes: [Node]) {
            self.nodes = nodes
        }
        
        func neighbor(of node: Node, dir: Dir) -> Node {
            if dir == Dir.Right {
                return self.node(toRightOf: node)
            } else {
                return self.node(toLeftOf: node)
            }
        }
        
        func node(toRightOf: Node) -> Node {
            if let right = toRightOf.right {
                return right
            }
            
            // Add new linked node
            let newNode = Node()
            newNode.left = toRightOf
            toRightOf.right = newNode
            
            // Retain strong ref
            self.nodes.append(newNode)
            return newNode
        }
        
        func node(toLeftOf: Node) -> Node {
            if let left = toLeftOf.left {
                return left
            }
            
            // Add new linked node
            let newNode = Node()
            newNode.right = toLeftOf
            toLeftOf.left = newNode
            
            // Retain strong ref
            self.nodes.append(newNode)
            return newNode
        }
        
        func checksum() -> Int {
            return nodes.reduce(0, { acc, node in acc + node.value })
        }
    }
    
    class Node {
        var value: Int = 0
        weak var left: Node?
        weak var right: Node?
    }
    
    private static func parseBlueprint(from lines: [String]) -> Blueprint {
        var match = lines[0].firstMatch(of: /Begin in state (.*)./)!
        let startState = String(match.output.1)
        
        match = lines[1].firstMatch(of: /checksum after (.*) steps./)!
        let diagnosticStep = Int(match.output.1)!
        
        var actionMap: [String: Action] = [:]
        var i = 3
        while i < lines.count {
            let match = lines[i].firstMatch(of: /^In state (.*):/)!
            let state = String(match.output.1)
            
            actionMap[mapKey(state, 0)] = parseAction(from: lines, idx: i+2)
            actionMap[mapKey(state, 1)] = parseAction(from: lines, idx: i+6)
            
            i += 10
        }
        
        return Blueprint(
            startState: startState,
            diagnosticStep: diagnosticStep,
            actionMap: actionMap
        )
    }
    
    private static func parseAction(from lines: [String], idx: Int) -> Action {
        var match = lines[idx].firstMatch(of: /the value (.*)./)!
        let writeValue = Int(match.output.1)!
        
        match = lines[idx+1].firstMatch(of: /to the (.*)./)!
        let moveDir = match.output.1 == "right" ? Dir.Right : Dir.Left
        
        match = lines[idx+2].firstMatch(of: /state (.*)./)!
        let nextState = String(match.output.1)
        
        return Action(writeValue: writeValue, moveDir: moveDir, nextState: nextState)
    }
            
    private static func mapKey(_ state: String, _ val: Int) -> String {
        return "\(state),\(val)"
    }
    
    struct Blueprint {
        let startState: String
        let diagnosticStep: Int
        let actionMap: [String: Action]
    }
    
    struct Action {
        let writeValue: Int
        let moveDir: Dir
        let nextState: String
    }
    
    enum Dir {
        case Left;
        case Right;
    }
}
