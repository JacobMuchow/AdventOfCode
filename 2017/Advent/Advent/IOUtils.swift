//
//  File.swift
//  Advent
//
//  Created by Jacob Muchow on 9/3/24.
//

import Foundation

class IOUtils {
    static func readLinesFromFile(_ relativePath: String, removingLast: Bool = true) -> [String] {
        let currentDir = URL(fileURLWithPath: FileManager.default.currentDirectoryPath)
        let fileURL = currentDir.appendingPathComponent(relativePath)

        do {
            let content = try! String(contentsOf: fileURL, encoding: .utf8)
            var lines = content.components(separatedBy: .newlines)
            
            if removingLast {
                _ = lines.popLast()
            }
            
            return lines
        }
    }
}
