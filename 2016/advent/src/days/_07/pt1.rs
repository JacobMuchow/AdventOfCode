// #![allow(dead_code)]

use crate::shared::io::read_lines_from_file;

pub fn run() {
    let lines = read_lines_from_file("src/days/_07/input.txt");
    for line in lines {
        println!("{}", line);
    }
}