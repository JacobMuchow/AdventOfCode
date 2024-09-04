import Foundation

class Day03Pt1 {
    // This will give us a Cartesian coordinate position for the
    // data. Where "1" corresponds to (0, 0) and Up/Right are positive
    // (like in your math class).
    static func findTargetPos(_ target: Int) -> (Int, Int) {
        // The spiral grows by odd squares in the bottom-right corner...
        // 1 -> 9 -> 25 -> 49 ...
        // This allows us to easily compute in which "layer" of the spiral
        // the target data will be. Then we can do some (annoying) logic
        // trace backwards to the coordinates of the data.
        var i = 1
        while i*i < target {
            i += 2
        }
        
        let brCorner = i*i
        let disToPrevCorner = i-1
        
        // 9  (i=3) -> 1 layer
        // 25 (i=5) -> 2 layers
        // 49 (i=7) -> 3 layers...
        let layerCount = (i-1) / 2
        
        // Conveniently, the target data is the bottom-right corner value.
        if brCorner == target {
            return (layerCount, -layerCount)
        }
        
        // Check bottom row to BL corner
        let blCorner = brCorner - disToPrevCorner
        if (target >= blCorner) {
            return (-layerCount + (target-blCorner), -layerCount)
        }
        
        // Check left row to TL corner
        let tlCorner = blCorner - disToPrevCorner
        if target >= tlCorner {
            return (-layerCount, layerCount - (target-tlCorner))
        }
        
        // Check top row to TR corner
        let trCorner = tlCorner - disToPrevCorner
        if target >= trCorner {
            return (layerCount - (target-trCorner), layerCount)
        }
        
        // Check right row to just before BR corner
        let brCornerPrev = trCorner - disToPrevCorner
        if target <= brCornerPrev {
            fatalError("Something went horribly wrong!")
        }
        
        return (layerCount, -layerCount + (target-brCornerPrev))
    }
    
    static func run() {
        let lines = IOUtils.readLinesFromFile("day03_input.txt")

        let target = Int(lines[0], radix: 10)!
        print("Target: \(target)")
        
        let (x, y) = findTargetPos(target)
        let dis = abs(x) + abs(y)
        
        print("Num steps: \(dis)")
    }
}
