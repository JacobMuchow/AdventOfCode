//
//  Day23Pt2.swift
//  Advent
//
//  Created by Jacob Muchow on 12/5/25.
//

class Day23Pt2 {
    static func run() {
        /*
         Initially I was trying to optimize the assembly code by adding some custom instructions
         / handlers which served me on some similar problems in the past. But gave up on this path
         when I realized the f/h flags would not get set properly.
         
         For this problem, I ended up translating the code to a more modern format
         (a few times... not pictured) until I could understand the intent. Eventually
         you learn it is checking NOT-prime numbers ("composite" numbers) in range b-c with
         a step of 17.
         
         Or at least that's what you should do. To my shame I resorted to reddit for hints. But
         I've gone back through to understand the assembly now at least. Half a star?
         
         b = 79
         c = 79
         b *= 100
         b += 100_000
         c = b + 17_000

         while b <= c {
             f = 1
             d = 2
                     
             // check every combination of numbers 2..n for d,e divises into
             while {
                 e = 2
                 
                 // if any divises cleanly, then f = 0
                 g = d*e - b
                 if (g == 0) f = 0
                 
                 e += 1
                 g = e-b
                 if (g != 0) go up 5 lines
                 
                 d += 1
                 g = d-b
                 if (g == 0) break;
             }

             if (f == 0) h += 1
             b += 17
         }
         */
        
        
        var b = 79
        var c = 0
        var h = 0
        
        b = b * 100 + 100_000
        c = b + 17_000
        
        while b <= c {
            if (isComposite(num: b)) {
                h += 1
            }
            b += 17
        }
    
        print("h: \(h)")
    }
    
    private static func isComposite(num: Int) -> Bool {
        // Not very good way to check for composite/prime, but it's sub 1-second for the problem so I'm not worrying.
        for d in 2...num/2 {
            if (num % d == 0) {
                return true
            }
        }
        return false
    }
}
