#![allow(dead_code)]

use crate::shared::io::read_lines_from_file;

fn supports_tls(line: &String) -> bool {
    let chars: Vec<char> = line.chars().collect();
    
    let mut in_hyperlink = false;
    let mut has_abba = false;

    for i in 0..chars.len() {
        // Handle hyperlink scope
        if !in_hyperlink && *chars.get(i).unwrap() == '[' {
            in_hyperlink = true;
            continue;
        } else if in_hyperlink && *chars.get(i).unwrap() == ']' {
            in_hyperlink = false;
            continue;
        }

        // this would lead to OOB.
        if i < 3 {
            continue;
        }

        // Optimization
        if has_abba && !in_hyperlink {
            continue;
        }

        // ABBA check
        let char1 = *chars.get(i-3).unwrap();
        let char2 = *chars.get(i-2).unwrap();
        let char3 = *chars.get(i-1).unwrap();
        let char4 = *chars.get(i).unwrap();

        if char1 == '[' || char2 == ']' || char3 == '[' || char4 == ']' {
            continue;
        }

        if char1 == char4 && char2 == char3 && char1 != char2 {
            if in_hyperlink {
                return false;
            }
            has_abba = true;
        }
    }

    return has_abba;
}

pub fn run() {
    let lines = read_lines_from_file("src/days/_07/input.txt");

    let mut count_valid = 0;
    for line in lines {
        let valid = supports_tls(&line);
        if valid {
            count_valid += 1;
        }
    }

    println!("Number supporting TLS: {}", count_valid);
}