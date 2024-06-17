#![allow(dead_code)]

use crate::shared::io::read_lines_from_file;

fn supports_ssl(line: &String) -> bool {
    let chars: Vec<char> = line.chars().collect();
    
    let mut in_hyperlink = false;
    let mut supernet_abas = Vec::<String>::new();
    let mut hyperlink_abas = Vec::<String>::new();

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
        if i < 2 {
            continue;
        }

        // ABA check
        let char1 = *chars.get(i-2).unwrap();
        let char2 = *chars.get(i-1).unwrap();
        let char3 = *chars.get(i).unwrap();

        if char1 == '[' || char1 == ']' || char2 == '[' || char2 == ']' {
            continue;
        }

        if char1 == char3 && char1 != char2 {
            let aba = format!("{}{}{}", char1, char2, char3);
            if in_hyperlink {
                hyperlink_abas.push(aba);
            } else {
                supernet_abas.push(aba);
            }
        }
    }

    for aba in &supernet_abas {
        let chars: Vec<char> = aba.chars().collect();
        let char1 = *chars.get(0).unwrap();
        let char2 = *chars.get(1).unwrap();
        
        let bab = format!("{}{}{}", char2, char1, char2);
        
        for aba2 in &hyperlink_abas {
            if *aba2 == bab {
                return true;
            }
        }
    }

    return false;
}

pub fn run() {
    let lines = read_lines_from_file("src/days/_07/input.txt");

    let mut count_valid = 0;
    for line in lines {
        let valid = supports_ssl(&line);
        if valid {
            count_valid += 1;
        }
    }

    println!("Number supporting SSL: {}", count_valid);
}