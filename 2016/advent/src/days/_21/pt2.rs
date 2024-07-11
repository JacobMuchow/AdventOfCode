#![allow(dead_code)]

use regex::Regex;

use crate::shared::{io::read_lines_from_file, regex_extensions::ExtensionsTrait};

#[derive(PartialEq, Eq)]
enum Dir {
    Left,
    Right
}

fn rotate(str: &Vec<char>, dir: Dir, shift: usize) -> Vec<char> {
    let mut new_str: Vec<char> = Vec::with_capacity(str.len());

    let split_i = if dir == Dir::Left {
        shift % str.len()
    } else {
        str.len() - (shift % str.len())
    };

    let (a, b) = str.split_at(split_i);
    new_str.extend_from_slice(b);
    new_str.extend_from_slice(a);

    new_str
}

pub fn rotate_by_letter(str: &Vec<char>, letter: char) -> Vec<char> {
    let pos = str.iter().position(|c| *c == letter).unwrap();
    let shift = pos + (if pos >= 4 { 2 } else { 1 });

    rotate(&str, Dir::Right, shift)
}

pub fn rotate_by_letter_reversed(str: &Vec<char>, letter: char) -> Vec<char> {
    // Test Left rotations of str until we get one that fulfills the original rotation command.

    let mut test = str.clone();

    loop {
        test = rotate(&test, Dir::Left, 1);

        let out = rotate_by_letter(&test, letter);
        if &out == str {
            return test
        }
    }
}

pub fn run() {
    // let lines = read_lines_from_file("src/days/_21/test.txt");
    // let mut password: Vec<char> = "abcde".chars().collect();

    let mut lines = read_lines_from_file("src/days/_21/input.txt");
    // let mut password: Vec<char> = "baecdfgh".chars().collect(); // expect "abcdefgh"
    let mut password: Vec<char> = "fbgdceah".chars().collect();

    lines.reverse();

    for line in &lines {
        let str: String = password.iter().collect();
        println!("{}: {}", str, line);

        // No change.
        let re = Regex::new(r"^swap position ([0-9]+) with position ([0-9]+)").unwrap();
        if let Some(caps) = re.captures(&line) {
            let x: usize = caps.get_as_num(1).unwrap();
            let y: usize = caps.get_as_num(2).unwrap();

            let swap = password[x];
            password[x] = password[y];
            password[y] = swap;
            continue;
        }

        // No change.
        let re = Regex::new(r"^swap letter ([A-Za-z]) with letter ([A-Za-z])").unwrap();
        if let Some(caps) = re.captures(&line) {
            let x = caps.get_as_char(1).unwrap();
            let y = caps.get_as_char(2).unwrap();

            for i in 0..password.len() {
                if password[i] == x {
                    password[i] = y;
                } else if password[i] == y {
                    password[i] = x;
                }
            }
            continue;
        }

        // Done.
        let re = Regex::new(r"^rotate (left|right) ([0-9]+)").unwrap();
        if let Some(caps) = re.captures(&line) {
            let dir_raw = caps.get_as_str(1).unwrap();
            let shift: usize = caps.get_as_num(2).unwrap();

            let dir = if dir_raw == "right" { Dir::Left } else { Dir::Right };

            password = rotate(&password, dir, shift);
            continue;
        }

        let re = Regex::new(r"^rotate based on position of letter ([A-Za-z])").unwrap();
        if let Some(caps) = re.captures(&line) {
            let x = caps.get_as_char(1).unwrap();
            password = rotate_by_letter_reversed(&password, x);
            continue;
        }

        // No change.
        let re = Regex::new(r"^reverse positions ([0-9]+) through ([0-9]+)").unwrap();
        if let Some(caps) = re.captures(&line) {
            let x: usize = caps.get_as_num(1).unwrap();
            let y: usize = caps.get_as_num(2).unwrap();

            let old_pass = password.clone();
            let diff = y - x;

            for i in 0..=diff {
                password[x+i] = old_pass[y-i];
            }

            continue;
        }

        // Done.
        let re = Regex::new(r"^move position ([0-9]+) to position ([0-9]+)").unwrap();
        if let Some(caps) = re.captures(&line) {
            let x: usize = caps.get_as_num(1).unwrap();
            let y: usize = caps.get_as_num(2).unwrap();

            let c = password.remove(y);
            password.insert(x, c);
            continue;
        }

        panic!("Unknown instruction: {}", line);
    }

    let pass: String = password.iter().collect();
    println!("Final password: {}", pass);
}