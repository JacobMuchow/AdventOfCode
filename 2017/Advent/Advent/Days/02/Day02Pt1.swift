import Foundation

class Day02Pt1 {
    static func run() {
        let lines = IOUtils.readLinesFromFile("day02_input.txt")
        
        var total = 0

        for line in lines {
            let tokens = line.components(separatedBy: .whitespaces).filter { !$0.isEmpty }
            
            var low = Int.max
            var high = 0
            
            for token in tokens {
                guard let val = Int(token, radix: 10) else {
                    print("Failed to parse number from token: \(token)")
                    fatalError()
                }
                
                low = min(low, val)
                high = max(high, val)
            }
            
            let diff = high - low
            print("Diff: \(diff)")
            total += diff
        }
        
        print("Checksum: \(total)")
    }
}
