import Foundation

class Day03Pt2 {
    enum Dir {
        case R;
        case U;
        case L;
        case D;
    }
    
    typealias Pos2d = (Int, Int)

    static func nextDir(_ dir: Dir) -> Dir {
        switch dir {
        case Dir.R: return Dir.U;
        case Dir.U: return Dir.L;
        case Dir.L: return Dir.D;
        case Dir.D: return Dir.R;
        }
    }
    
    static func nextPos(_ pos: Pos2d, dir: Dir) -> Pos2d {
        let (x, y) = pos
        
        switch dir {
        case Dir.R: return (x+1, y)
        case Dir.L: return (x-1, y)
        case Dir.U: return (x, y+1)
        case Dir.D: return (x, y-1)
        }
    }
    
    static func keyForPos(_ pos: Pos2d) -> String {
        return "\(pos.0),\(pos.1)"
    }
    
    static func calculateValue(_ pos: Pos2d, written: [String: Int]) -> Int {
        let (x, y) = pos
        var total = 0
        
        // Sum all values of written neighboring values.
        total += written[keyForPos((x-1, y-1))] ?? 0
        total += written[keyForPos((x,   y-1))] ?? 0
        total += written[keyForPos((x+1, y-1))] ?? 0
        total += written[keyForPos((x-1, y))] ?? 0
        total += written[keyForPos((x+1, y))] ?? 0
        total += written[keyForPos((x-1, y+1))] ?? 0
        total += written[keyForPos((x,   y+1))] ?? 0
        total += written[keyForPos((x+1, y+1))] ?? 0
        
        return total
    }
    
    static func run() {
        let lines = IOUtils.readLinesFromFile("day03_input.txt")

        let target = Int(lines[0], radix: 10)!
        print("Target: \(target)")
        
        var written: [String: Int] = [
            "0,0": 1,
        ]
        
        var pos = (1, 0)
        var layerCount = 1
        var dir = Dir.U
        
        while true {
            
            // Sanity check... if a value has already been written
            // for this pos, something has gone wrong.
            let posKey = keyForPos(pos)
            if written[posKey] != nil {
                fatalError("Uh oh! Something went horribly wrong!")
            }
            
            // Calculate new value
            let value = calculateValue(pos, written: written)
            print("Value at \(posKey): \(value)")
            
            if value > target {
                return;
            }
            
            written[posKey] = value
            
            
            // If we're curently at any corner but BR... need to change direction.
            if (pos.0 == layerCount && pos.1 == layerCount) // TR corner
                || (pos.0 == -layerCount && abs(pos.1) == layerCount) // TL+BL corner spiral
            {
                dir = nextDir(dir)
            }
            
            // Start of new spiral
            else if pos.0 == layerCount+1 && pos.1 == -layerCount {
                dir = nextDir(dir)
                layerCount += 1
            }
            
            // Move to new pos
            pos = nextPos(pos, dir: dir)
        }
    }
}
