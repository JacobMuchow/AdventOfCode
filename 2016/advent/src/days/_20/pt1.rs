#![allow(dead_code)]

use crate::shared::io::read_lines_from_file;

pub fn run() {
    let lines = read_lines_from_file("src/days/_20/input.txt");

    let mut ranges: Vec<(u32, u32)> = Vec::with_capacity(lines.len());

    for line in &lines {
        let splits: Vec<&str> = line.split('-').collect();
        let left: u32 = splits[0].parse().unwrap();
        let right: u32 = splits[1].parse().unwrap();
        ranges.push((left, right));
    }

    let mut test_valid: u32 = 0;

    'outer: loop {
        for range in &ranges {
            // Intersects with some range
            if test_valid >= range.0 && test_valid <= range.1 {
                test_valid = range.1+1;
                continue 'outer;
            }
        }
        break;
    }

    println!("Min usable: {}", test_valid);
}