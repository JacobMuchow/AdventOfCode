//
//  Day21Pt2.swift
//  Advent
//
//  Created by Jacob Muchow on 12/5/25.
//

class Day23Pt2 {
    static var registers: [String:Int] = [
        "a": 1,
        "h": 0,
    ]
    static let isRegisterRegex = try! Regex("^[A-Za-z]")
    
    static func run() {
        let lines = IOUtils.readLinesFromFile("day23_input2.txt")
        
        var pos = 0
        var maxPos = 0
        var i = 0
        
        // a = 1
        // b = 107900
        // c = 107900 - 17000
        // f = 1
        //
        // {
        //   d = 2
        //   e = 2
        //
        //
        
        // }

        /*
         a = 1
         b = 107,900
         c = 107,900 - 17,000
         f = 1
         
         {
            d = 2
            e =  2
            while (true) {
                g = (d*e) - b
                if (g == 0) f -> 0
                e++
                g = e-b
                if (g == 0) break
            }
         
            d++
            g = d-b
            if g != 0 --> goto "e = 2"
            
         }
         
         if f == 0 -> h++
         
         g = b-c
         if (g != 0) {
           b -= 17
           goto -> "f = 1"
         }
         exit;
         */
        
        while pos >= 0 && pos < lines.count {
            maxPos = max(maxPos, pos)
            i += 1
            
            let tokens = lines[pos].split(separator: " ")
            let cmd = tokens[0]
            
            if (i % 10_000 == 0) {
                print("\(i)")
            }

            
            
            
            
//            if pos == 11 {
//                let b = registers["b", default: 0]
//                let d = registers["d", default: 0]
//                let e = registers["e", default: 0]
//                let g = registers["g", default: 0]
//                print("\(lines[pos]): b (\(b)) d(\(d)) e (\(e)) g (\(g)) maxPos (\(maxPos))")
//
//                // h++
//                // g = b - c
//                // if g == 0 --> exit
//                // else b += 17
//                // jt --> 9
//            }
//            
            switch cmd {
            case "fn1":
                let b = valueFor(input: "b")
                let d = valueFor(input: "d")
                let e = valueFor(input: "e")
                
                
                // g = d*e - b
                // if g = 0 --> f = 0
                // e = b/c
                // loop e++
                
                // e = 2
                // b = 107000
                // d = 2
                // g = d*e - b
                // b / d = e
                
                if d >= e && d <= b {
                    registers["f"] = 0
                }
//                registers["f"] = 0
                registers["e"] = b
                registers["g"] = 0
                break
                
            case "fn2":
                registers["d"] = valueFor(input: "d") + 1
                registers["g"] = valueFor(input: "d") - valueFor(input: "b")
                if registers["g"] != 0 {
                    pos = 10
                }
                break
                
            case "set":
                let reg = String(tokens[1])
                let val = valueFor(input: String(tokens[2]))
                registers[reg] = val
                break
                
            case "sub":
                let reg = String(tokens[1])
                let val = valueFor(input: String(tokens[2]))
                registers[reg] = registers[reg, default: 0] - val
                break
                
            case "mul":
                let reg = String(tokens[1])
                let val = valueFor(input: String(tokens[2]))
                registers[reg] = registers[reg, default: 0] * val
                break
            
            case "jnz":
                let valX = valueFor(input: String(tokens[1]))
                if valX != 0 {
                    let valY = valueFor(input: String(tokens[2]))
                    pos += valY
                    continue
                }
                break
                
            default:
                fatalError("Unknown command: \(cmd)")
            }
            
            pos += 1
        }
    
        print("Program exited.")
        print("h register: \(registers["h"]!)")
    }
    
    static func valueFor(input: String) -> Int {
        if let _ = try! isRegisterRegex.prefixMatch(in: input) {
            return registers[input, default: 0]
        } else {
            return Int(input)!
        }
    }
}
