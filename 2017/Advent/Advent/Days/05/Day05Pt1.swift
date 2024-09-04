import Foundation

class Day05Pt1 {
    static func run() {
        let lines = IOUtils.readLinesFromFile("day05_input.txt")
        
        var jumps = lines.map { Int($0, radix: 10)! }
        var lineNum = 0
        var numSteps = 0
        
        while lineNum < jumps.count {
            let newLine = lineNum + jumps[lineNum]
            jumps[lineNum] += 1
            lineNum = newLine
            numSteps += 1
        }
        
        print("Maze exited. Num steps: \(numSteps)")
    }
}
