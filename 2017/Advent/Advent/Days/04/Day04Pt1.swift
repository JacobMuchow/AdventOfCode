import Foundation

class Day04Pt1 {
    static func isValidPassphrase(_ passphrase: String) -> Bool {
        var tokenMap: [String: Bool] = [:]
        
        let tokens = passphrase.split(separator: " ").map { String($0) }
        for token in tokens {
            if tokenMap[String(token)] ?? false {
                return false;
            }
            tokenMap[token] = true;
        }
        return true;
    }
    
    static func run() {
        let lines = IOUtils.readLinesFromFile("day04_input.txt")
        
        var numValid = 0
        
        for line in lines {
            if isValidPassphrase(line) {
                numValid += 1
            }
        }
        
        print("Num valid: \(numValid)")
    }
}
