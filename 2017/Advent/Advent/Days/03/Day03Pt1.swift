import Foundation

class Day03Pt1 {
    static func findTargetPos(_ target: Int) -> Int {
        // The spiral grows by the odd squares in the bottom-right corner...
        // 1 -> 9 -> 25 -> 49 ...
        var i = 1
        while i*i <= target {
            i += 2
        }
        
        // 9  (i=3) -> 1 layer
        // 25 (i=5) -> 2 layers
        // 49 (i=7) -> 3 layers...
        let layerCount = (i-1) / 2
        
        var cornerVal = i*i
        var disToPrevCorner = i-1
        
        print("i value found: \(i)")
        print("Layer count: \(layerCount)")
        print("bottom-right corner: \(cornerVal)")
        
        while cornerVal > target {
            cornerVal -= disToPrevCorner;
        }
        
        let cornerDisToCenter = layerCount * 2
        let cornerDisToTarget = target - cornerVal
        
        print("Corner val prior to target: \(cornerVal)")
        print("Dis corner to center: \(cornerDisToCenter)")
        print("Dis corner to target: \(cornerDisToTarget)")
        
        let targetDisToCenter = cornerDisToCenter - cornerDisToTarget
        print("Target dis to center: \(targetDisToCenter)")
        
        return targetDisToCenter
    }
    
    static func run() {
//        let lines = IOUtils.readLinesFromFile("day03_input.txt")
//
//        let target = Int(lines[0], radix: 10)!
        
        let target = 12;
        print("Target: \(target)")
        
        let dis = findTargetPos(target)
        print("Dis: \(dis)")
    }
}
