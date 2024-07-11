#![allow(dead_code)]

use regex::{Regex};

use crate::shared::{io::read_lines_from_file, regex_extensions::ExtensionsTrait};

pub fn run() {
    let lines = read_lines_from_file("src/days/_21/test.txt");
    let mut password: Vec<char> = "abcde".chars().collect();

    for line in &lines {
        let re = Regex::new(r"swap position ([0-9]+) with position ([0-9]+)").unwrap();
        if let Some(caps) = re.captures(&line) {
            let x: usize = caps.get_as_num(1).unwrap();
            let y: usize = caps.get_as_num(2).unwrap();

            let swap = password[x];
            password[x] = password[y];
            password[y] = swap;
            continue;
        }

        let re = Regex::new(r"swap letter ([A-Za-z]) with letter ([A-Za-z])").unwrap();
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

        let re = Regex::new(r"rotate (left|right) ([0-9]+) steps").unwrap();
        if let Some(caps) = re.captures(&line) {
            let x = caps.get_as_str(1).unwrap();
            let y: usize = caps.get_as_num(2).unwrap();

            // todo...
            continue;
        }
    }
}