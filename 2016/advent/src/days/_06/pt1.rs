// #![allow(dead_code)]

use crate::shared::io::read_lines_from_file;

pub fn run() {
    let lines = read_lines_from_file("src/days/_06/test.txt");
    for line in lines {
        println!("{}", line);
    }
}