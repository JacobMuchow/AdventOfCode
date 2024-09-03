//
//  main.swift
//  Advent
//
//  Created by Jacob Muchow on 9/3/24.
//

import Foundation

print("Hello, World!")

let currentDir = URL(fileURLWithPath: FileManager.default.currentDirectoryPath)

print("Current dir: \(currentDir.absoluteString)")

let fileURL = currentDir.appendingPathComponent("input.txt")

print("File URL: \(fileURL)")

do {
    let content = try String(contentsOf: fileURL, encoding: .utf8)
    print(content)
} catch {
    print("Error reading file: \(error.localizedDescription)")
}
