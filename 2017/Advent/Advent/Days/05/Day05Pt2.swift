import Foundation

class Day05Pt2 {
    static func run() {
        let lines = IOUtils.readLinesFromFile("day05_input.txt")
        
        var jumps = lines.map { Int($0, radix: 10)! }
        var lineNum = 0
        var numSteps = 0
        
        while lineNum < jumps.count {
            let jump = jumps[lineNum]
            let newLine = lineNum + jump
            
            jumps[lineNum] += jump >= 3 ? -1 : 1
            lineNum = newLine
            numSteps += 1
        }
        
        print("Maze exited. Num steps: \(numSteps)")
    }
}
