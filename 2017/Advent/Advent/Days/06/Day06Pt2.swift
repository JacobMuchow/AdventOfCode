import Foundation

class Day06Pt2 {
    static func redistribute(_ banks: [Int]) -> [Int] {
        var banks_out = banks
        
        // First, find which bank is largest
        var max_idx = 0
        
        for i in 1..<banks.count {
            if banks[i] > banks[max_idx] {
                max_idx = i
            }
        }
        
        // Redistribute the blocks
        var blocks = banks[max_idx]
        banks_out[max_idx] = 0
        
        var i = max_idx
        
        while blocks > 0 {
            i = (i+1) % banks.count
            banks_out[i] += 1
            blocks -= 1
        }
        
        return banks_out
    }
    
    static func banks_hash(_ banks: [Int]) -> String {
        return "\(banks)"
    }
    
    static func run() {
        let lines = IOUtils.readLinesFromFile("day06_input.txt")
    
        var banks = lines[0].split(separator: " ").map { Int($0, radix: 10)! }
        
        // Not hard, simply need to track the current cycle count when we add the visited
        // state to the dictionary.
        var visited: [String: Int] = [
            banks_hash(banks): 0
        ]
        
        var cycle_count = 0
        
        while true {
            banks = redistribute(banks)
            cycle_count += 1
            
            let hash = banks_hash(banks)
            if let prev_count = visited[hash] {
                let cycle_length = cycle_count - prev_count
                print("Cycle length: \(cycle_length)")
                break
            }
            visited[hash] = cycle_count
        }
    }
}
