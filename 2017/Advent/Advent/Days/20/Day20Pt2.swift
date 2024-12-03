//
//  Day20Pt2.swift
//  Advent
//
//  Created by Jacob Muchow on 12/2/24.
//

import Foundation

class Day20Pt2 {
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
        
        func toString() -> String {
            return "\(self.pos) \(self.vel) \(self.acc)"
        }
    }
    
    static func run() {
        let lines = IOUtils.readLinesFromFile("day20_test.txt")
        for line in lines {
            print(line)
        }
        
        // Parse input into Particle objects.
        let particles = parseParticles(lines: lines)
//        for particle in particles {
//            print("\(particle.pos) \(particle.vel) \(particle.acc)")
//        }
        
//        let t = calcCollisionTime(of: particles[0], with: particles[1])
//        print("Collision time: \(t)")
        
        print("Comp 0-1")
        _ = calcCollisionTime(of: particles[0], with: particles[1])
        
        print("\nComp 1-0")
        _ = calcCollisionTime(of: particles[1], with: particles[0])
        
        return
        
        var potentialCollisions: [Double:Set<Int>] = [:]
        
        for i in 0..<particles.count-1 {
            for j in i+1..<particles.count {
                if let time = calcCollisionTime(of: particles[i], with: particles[j]) {
                    var set = potentialCollisions[time, default: Set()]
                    set.insert(i)
                    set.insert(j)
                    potentialCollisions[time] = set
                }
            }
        }
        
        let sortedTimes = potentialCollisions.keys.sorted()
        print("Sorted times: \(sortedTimes)")
        

        // Filter collisions keeping track of which have already collided and ignoring any future collisions.
        var collidedParticles = Set<Int>()
        
        for time in sortedTimes {
            let potentials = potentialCollisions[time]!.filter({ !collidedParticles.contains($0) })
            if potentials.count > 1 {
                for p in potentials {
                    collidedParticles.insert(p)
                }
            }
        }
        
        print("Collided particles: \(collidedParticles)")
        
        let particlesLeft = particles.count - collidedParticles.count
        print("Particles left: \(particlesLeft)")
    }
    
    static func calcCollisionTime(of particleA: Particle, with particleB: Particle) -> Double? {
        print(particleA.toString())
        print(particleB.toString())
        let ax = particleA.acc.x - particleB.acc.x
        let bx = particleA.vel.x - particleB.vel.x
        let cx = particleA.pos.x - particleB.pos.x
        
        var timesX = calcTimesQuadratic(a: Double(ax), b: Double(bx), c: Double(cx))
        print("TimesX: \(timesX)")
            
        timesX = timesX.filter({ $0 > 0 })
        if timesX.isEmpty { return nil }
        
        let ay = particleA.acc.y - particleB.acc.y
        let by = particleA.vel.y - particleB.vel.y
        let cy = particleA.pos.y - particleB.pos.y
        
        var timesY = calcTimesQuadratic(a: Double(ay), b: Double(by), c: Double(cy))
        print("TimesY: \(timesY)")
        timesY = timesY.filter({ $0 > 0 })
        if timesY.isEmpty { return nil }
        
        let az = particleA.acc.z - particleB.acc.z
        let bz = particleA.vel.z - particleB.vel.z
        let cz = particleA.pos.z - particleB.pos.z
        
        var timesZ = calcTimesQuadratic(a: Double(az), b: Double(bz), c: Double(cz))
        print("TimesZ: \(timesZ)")
        timesZ = timesZ.filter({ $0 > 0 })
        if timesZ.isEmpty { return nil }
        
        let sortedTimes = timesX.sorted(by: { a,b in a < b })
        
        for time in sortedTimes {
            if timesY.filter({ $0 == time || $0 == Double.infinity }).count > 0 &&
                timesZ.filter({ $0 == time || $0 == Double.infinity }).count > 0 {
                return time
            }
        }
        
        return nil
    }
    
    static func calcTimesQuadratic(a: Double, b: Double, c: Double) -> [Double] {
        print("Calc times... a: \(a), b: \(b), c: \(c)")
        
        // Quadratic
        if a != 0 {
            let root = sqrt(b*b - 4*a*c)
            let nom = -b + root
            let dom = 2*a
//            print("root \(root) nom \(nom) dom \(dom)")
            return [
                (-b + root) / (2*a),
                (-b - root) / (2*a)
            ]
        }
        
        // Linear
        if b != 0 {
            return [-c/b]
        }
        
        return c == 0 ? [Double.infinity] : []
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
