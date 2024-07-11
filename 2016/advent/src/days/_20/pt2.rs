#![allow(dead_code)]

use crate::shared::io::read_lines_from_file;

fn next_valid_range_start(ranges: &Vec<(u32, u32)>, start_ip: u32) -> u32 {
    let mut test_valid = start_ip;

    'outer: loop {
        for range in ranges {
            // Intersects with some range
            if test_valid >= range.0 && test_valid <= range.1 {
                // Edge case, intersects with final blacklist range.
                if range.1 == u32::MAX {
                    return u32::MAX;
                }

                test_valid = range.1+1;
                continue 'outer;
            }
        }
        return test_valid;
    }
}

fn find_valid_range_end(ranges: &Vec<(u32, u32)>, start_ip: u32) -> u32 {
    let mut range_end = u32::MAX;
    
    for range in ranges {
        if range.1 < start_ip { 
            continue;
        }
        range_end = range_end.min(range.0-1);
    }

    range_end
}

pub fn run() {
    let lines = read_lines_from_file("src/days/_20/input.txt");

    let mut ranges: Vec<(u32, u32)> = Vec::with_capacity(lines.len());

    for line in &lines {
        let splits: Vec<&str> = line.split('-').collect();
        let left: u32 = splits[0].parse().unwrap();
        let right: u32 = splits[1].parse().unwrap();
        ranges.push((left, right));
    }

    let mut total_valid = 0;
    let mut known_start = next_valid_range_start(&ranges, 0);

    loop {
        let known_end = find_valid_range_end(&ranges, known_start);
        println!("Valid range: {} - {}", known_start, known_end);

        total_valid += known_end - known_start + 1;

        if known_end == u32::MAX {
            break;
        }

        known_start = next_valid_range_start(&ranges, known_end+1);
        if known_start == u32::MAX {
            break;
        }
    }

    println!("Total valid: {}", total_valid);
}