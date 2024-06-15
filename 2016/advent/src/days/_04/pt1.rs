use std::collections::HashMap;

use crate::shared::io::read_lines_from_file;
use regex::Regex;

fn is_decoy(name: String, checksum: String) -> bool {
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

    let mut sum = 0_u32;

    for (name, id, checksum) in codes {
        if !is_decoy(name, checksum) {
            sum += id;
        }
    }

    println!("Sum: {}", sum);
}