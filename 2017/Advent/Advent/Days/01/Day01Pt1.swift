import Foundation

class Day01Pt1 {
    static func run() {
        let lines = IOUtils.readLinesFromFile("day01_input.txt")

        let sequence = lines[0]
        var total = 0
        
        for i in 0..<sequence.count {
            let j = (i+1) % sequence.count
            
            let indexI = sequence.index(sequence.startIndex, offsetBy: i)
            let indexJ = sequence.index(sequence.startIndex, offsetBy: j)
            
            if sequence[indexI] == sequence[indexJ] {
                let val = sequence[indexI]
                let numVal = Int("\(val)", radix: 10)!

                total += numVal
            }
        }

        print("Total: \(total)")
    }
}
