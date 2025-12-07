//
//  Day25Pt1.swift
//  Advent
//
//  Created by Jacob Muchow on 12/5/25.
//

class Day25Pt1 {
    static func run() {
        let lines = IOUtils.readLinesFromFile("day25_test.txt")
        let blueprint = parseBlueprint(from: lines)
        
        print("Start state: \(blueprint.startState)")
        print("Checksum step: \(blueprint.diagnosticStep)")
        
        print("ACTIONS:")
        for (key, action) in blueprint.actionMap {
            print(key)
            print("* Write \(action.writeValue)")
            print("* Move \(action.moveDir)")
            print("* New state: \(action.nextState)\n")
        }
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
