//
//  Day20Pt1.swift
//  Advent
//
//  Created by Jacob Muchow on 12/2/24.
//

import Foundation

class Day20Pt1 {
    struct Vector3D {
        var x, y, z: Int
    }
    
    class Particle {
        var pos: Vector3D
        var vel: Vector3D
        var acc: Vector3D
        
        init(pos: Vector3D, vel: Vector3D, acc: Vector3D) {
            self.pos = pos
            self.vel = vel
            self.acc = acc
        }
    }
    
    static func run() {
        let lines = IOUtils.readLinesFromFile("day20_input.txt")
        for line in lines {
            print(line)
        }
        
        // Parse input into Particle objects.
        let particles = parseParticles(lines: lines)
        for particle in particles {
            print("\(particle.pos) \(particle.vel) \(particle.acc)")
        }
        
        var nearestParticle = 0
        var minAcc = Double.greatestFiniteMagnitude
        
        for (i, particle) in particles.enumerated() {
            let accMagnitude = calcMagnitude(of: particle)
            if accMagnitude < minAcc {
                minAcc = accMagnitude
                nearestParticle = i
            }
        }
        
        print("Nearest particle long-term: \(nearestParticle)")
    }
    
    static func calcMagnitude(of particle: Particle) -> Double {
        let acc = particle.acc
        let xSquared = acc.x * acc.x
        let ySquared = acc.y * acc.y
        let zSquared = acc.z * acc.z
        return sqrt(Double(xSquared + ySquared + zSquared))
    }
    
    static func parseParticles(lines: [String]) -> [Particle] {
        return lines.map { line in
            let tokens = line.components(separatedBy: ", ")
            
            return Particle(
                pos: parseVector3D(tokens[0]),
                vel: parseVector3D(tokens[1]),
                acc: parseVector3D(tokens[2])
            )
        }
    }
    
    static func parseVector3D(_ input: String) -> Vector3D {
        guard let match = input.firstMatch(of: /(-?\d+),(-?\d+),(-?\d+)/) else {
            fatalError("Failed to match vec3D from input: \(input)")
        }
        
        let (_, x, y, z) = match.output
        
        return Vector3D(
            x: Int(x, radix: 10)!,
            y: Int(y, radix: 10)!,
            z: Int(z, radix: 10)!
        )
    }
}
