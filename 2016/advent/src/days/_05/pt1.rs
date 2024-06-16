// #![allow(dead_code)]

use crate::shared::io::read_lines_from_file;
// use regex::Regex;

pub fn run() {
    let lines = read_lines_from_file("src/days/_05/test.txt");

    for line in lines {
        println!("{}", line);
    }
}