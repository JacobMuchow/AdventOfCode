import Foundation

class Day02Pt2 {
    static func findDivisible(_ numbers: [Int]) -> Int {
        print("Find divisible: \(numbers)")
        for i in 0..<numbers.count {
            for j in 0..<numbers.count {
                if i == j { continue }
                
                if numbers[i] % numbers[j] == 0 {
                    return numbers[i] / numbers[j]
                }
            }
        }
        
        fatalError("No even divisors found in set")
    }
    
    static func run() {
        let lines = IOUtils.readLinesFromFile("day02_input.txt")
        
        var total = 0

        for line in lines {
            let tokens = line.components(separatedBy: .whitespaces).filter { !$0.isEmpty }
            let numbers = tokens.map { Int($0, radix: 10)! }
        
            let value = findDivisible(numbers)
            
            print("Divise: \(value)")
            total += value
        }
        
        print("Checksum: \(total)")
    }
}
