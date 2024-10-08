import Foundation

class Day04Pt2 {
    static func anagramHash(_ word: String) -> String {
        var charCounts: [Character: Int] = [:]
        
        for idx in word.indices {
            let char = word[idx]
            charCounts[char] = (charCounts[char] ?? 0) + 1
        }
        
        let sortedChars = charCounts.keys.sorted()
        var hash = ""
        
        for char in sortedChars {
            hash += "\(char)\(charCounts[char]!)"
        }
        
        return hash
    }
    
    static func isValidPassphrase(_ passphrase: String) -> Bool {
        var anagramHashes: [String: Bool] = [:]
        
        let tokens = passphrase.split(separator: " ").map { String($0) }
        for token in tokens {
            let hash = anagramHash(token)
            
            if anagramHashes[hash] != nil {
                return false;
            }
            anagramHashes[hash] = true;
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
