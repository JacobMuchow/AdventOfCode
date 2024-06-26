#![allow(dead_code)]

use std::collections::HashMap;

use crate::shared::io::read_lines_from_file;

// Easy enough - just had to reverse the logic here from pt 1.
fn least_common_char(counts: &HashMap<char, u32>) -> char {
    let mut least_common: (char, u32) = (0 as char, u32::MAX);

    for entry in counts {
        if entry.1 < &least_common.1 {
            least_common = (*entry.0, *entry.1);
        }
    }

    return least_common.0;
}

pub fn run() {
    let lines = read_lines_from_file("src/days/_06/input.txt");

    let mut char_counts: Vec<HashMap<char, u32>> = Vec::new();
    let word_len = lines[0].len();

    for _ in 0..word_len {
        char_counts.push(HashMap::new());
    }

    for line in lines {
        let chars: Vec<char> = line.chars().collect();

        for i in 0..word_len {
            let char = chars[i];
            let count_map = char_counts.get_mut(i).unwrap();
            let count = count_map.get(&char).unwrap_or(&0) + 1;
            count_map.insert(char, count);
        }
    }

    let mut word = String::from("");
    for counts in &char_counts {
        word.push(least_common_char(counts));
    }

    println!("Word: '{}'", word);
}