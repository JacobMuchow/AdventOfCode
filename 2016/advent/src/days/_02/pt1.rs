#![allow(dead_code)]

use crate::shared::io::read_lines_from_file;

pub fn run() {
    let lines = read_lines_from_file("src/days/_02/input.txt");

    let keypad = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ];

    let mut x = 1_i32;
    let mut y = 1_i32;
    let mut keycode = String::from("");

    for line in lines {
        for char in line.chars() {
            match char {
                'R' => x = (x+1).min(2),
                'L' => x = (x-1).max(0),
                'U' => y = (y-1).max(0),
                'D' => y = (y+1).min(2),
                c @ _ => panic!("Unknown char in input: '{}'", c)
            }
        }

        keycode.push_str(&keypad[y as usize][x as usize].to_string());
    }

    println!("Keycode: {}", keycode);

}