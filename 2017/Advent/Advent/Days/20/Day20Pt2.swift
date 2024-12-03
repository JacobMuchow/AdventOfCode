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
        let id: Int
        var pos: Vector3D
        var vel: Vector3D
        var acc: Vector3D
        
        init(id: Int, pos: Vector3D, vel: Vector3D, acc: Vector3D) {
            self.id = id
            self.pos = pos
            self.vel = vel
            self.acc = acc
        }
        
        func toString() -> String {
            return "\(self.pos) \(self.vel) \(self.acc)"
        }
    }
    
    static func run() {
        let lines = IOUtils.readLinesFromFile("day20_input.txt")
        for line in lines {
            print(line)
        }
        
        let particles = parseParticles(lines: lines)
        
        // Simulate environment, this will exit on it's own when it's likely
        // no more collisions will occur.
        var particlesLeft = particles
        var time = 0
        var lastCollision = 0
        
        while true {
            time += 1
            
            if particlesLeft.isEmpty { break }
            
            // Stop simulation after there have been no collisions for 100 ticks.
            // This isn't technically perfect, but works for this problem.
            if time-lastCollision > 100 {
                break
            }
            
            print("Tick \(time)")
            let updatedList = tick(particles: particlesLeft)
            
            // Track time of last collision by comparing in/out list counts.
            if updatedList.count != particlesLeft.count {
                lastCollision = time
            }
            particlesLeft = updatedList
        }
        
        print("Num particles left: \(particlesLeft.count)")
    }

    static func tick(particles: [Particle]) -> [Particle] {
        // Step every particle forward 1 tick.
        for particle in particles {
            tick(particle: particle)
        }
        
        // Build set of which particles have collided by ID (number).
        var collided = Set<Int>()
        
        for i in 0..<particles.count-1 {
            for j in i+1..<particles.count {
                let iParticle = particles[i]
                let jParticle = particles[j]
                
                let iPos = iParticle.pos
                let jPos = jParticle.pos
                
                // Particles have collided if positions match after all have ticked forward.
                if iPos.x == jPos.x && iPos.y == jPos.y && iPos.z == jPos.z {
                    collided.insert(particles[i].id)
                    collided.insert(particles[j].id)
                }
            }
        }
    
        // Return list of remaining particles.
        return particles.filter({ !collided.contains($0.id)})
    }
    
    static func tick(particle: Particle) {
        // Update vel vector
        particle.vel.x += particle.acc.x
        particle.vel.y += particle.acc.y
        particle.vel.z += particle.acc.z
        
        // Update pos vector
        particle.pos.x += particle.vel.x
        particle.pos.y += particle.vel.y
        particle.pos.z += particle.vel.z
    }
    
    static func parseParticles(lines: [String]) -> [Particle] {
        var particles: [Particle] = []
        
        for i in 0..<lines.count {
            let tokens = lines[i].components(separatedBy: ", ")
            
            particles.append(Particle(
                id: i,
                pos: parseVector3D(tokens[0]),
                vel: parseVector3D(tokens[1]),
                acc: parseVector3D(tokens[2])
            ))
        }
        
        return particles
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
