#![allow(dead_code)]

use std::collections::HashMap;

use crate::shared::io::read_lines_from_file;
use regex::Regex;

// Unchanged from pt 1
fn is_decoy(name: &String, checksum: String) -> bool {
    let mut counts: HashMap<char, u32> = HashMap::new();

    for c in name.chars() {
        if c == '-' { continue; }
        let count = counts.get(&c).unwrap_or(&0) + 1;
        counts.insert(c, count);
    }

    let mut keys: Vec<&char> = counts.keys().collect();
    if keys.len() < checksum.len() {
        return true;
    }

    keys.sort_by(|a, b| {
        let count_a = counts.get(&a).unwrap();
        let count_b = counts.get(&b).unwrap();
        let cmp = count_b.cmp(count_a);

        if cmp != std::cmp::Ordering::Equal {
            return cmp;
        }
        return a.cmp(b);
    });

    for i in 0..checksum.len() {
        if *keys[i] != checksum.chars().nth(i).unwrap() {
            return true;
        }
    }

    return false;
}

fn decode(name: &String, id: u32) -> String {
    let mut decoded = "".to_string();

    for c in name.chars() {
        if c == '-' {
            decoded.push(' ');
            continue;
        }

        let c_val = c as u32;
        let a_val = 'a' as u32;
        let z_val = 'z' as u32;

        let mut shift = id;
        if c_val + shift <= z_val {
            decoded.push((c_val + shift) as u8 as char);
        } else {
            shift -= z_val-c_val+1; //+1 for inclusive
            shift %= z_val-a_val+1;
            decoded.push((a_val + shift) as u8 as char);
        }
    }

    return decoded;
}

pub fn run() {
    let lines = read_lines_from_file("src/days/_04/input.txt");

    let mut codes: Vec<(String, u32, String)> = Vec::new();
    let re = Regex::new(r"(.*)-([0-9]+)\[(.*)\]").unwrap();

    for line in lines {
        let caps = re.captures(&line).unwrap();

        codes.push((
            caps[1].to_string(),
            caps[2].parse().unwrap(), 
            caps[3].to_string()
        ));
    }

    // Gives many outputs, but easy enough to ctrl+F for "north"
    for (name, id, checksum) in codes {
        if !is_decoy(&name, checksum) {
            let decoded = decode(&name, id);
            println!("{} - {}", decoded, id);
        }
    }
}