import Foundation

class Day06Pt1 {
    static func redistribute(_ banks: [Int]) -> [Int] {
        var banks_out = banks
        
        // First, find which bank is largest
        var max_idx = 0
        
        for i in 1..<banks.count {
            if banks[i] > banks[max_idx] {
                max_idx = i
            }
        }
        
//        print("Banks: \(banks)")
//        print("Largest bank: #\(max_idx), val: \(banks[max_idx])")
        
        // Redistribute the blocks
        var blocks = banks[max_idx]
        banks_out[max_idx] = 0
        
        var i = max_idx
        
        while blocks > 0 {
            i = (i+1) % banks.count
            banks_out[i] += 1
            blocks -= 1
        }
        
//        print("Redistributed: \(banks_out)")
        
        return banks_out
    }
    
    static func banks_hash(_ banks: [Int]) -> String {
        return "\(banks)"
    }
    
    static func run() {
        let lines = IOUtils.readLinesFromFile("day06_input.txt")
    
        var banks = lines[0].split(separator: " ").map { Int($0, radix: 10)! }
        
        var visited: [String: Bool] = [
            banks_hash(banks): true
        ]
        
        var cycle_count = 0
        
        while true {
            banks = redistribute(banks)
            cycle_count += 1
            
            let hash = banks_hash(banks)
            if visited[hash] != nil {
                break
            }
            visited[hash] = true
        }
        
        print("Num cycles until repeat: \(cycle_count)")
    }
}
