//
//  File.swift
//  Advent
//
//  Created by Jacob Muchow on 9/3/24.
//

import Foundation

class IOUtils {
    static func readLinesFromFile(_ relativePath: String) -> [String] {
        let currentDir = URL(fileURLWithPath: FileManager.default.currentDirectoryPath)
        let fileURL = currentDir.appendingPathComponent(relativePath)

        do {
            let content = try! String(contentsOf: fileURL, encoding: .utf8)
            return content.components(separatedBy: .newlines)
        }
    }
}
