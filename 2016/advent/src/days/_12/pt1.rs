#![allow(dead_code)]

use std::collections::HashMap;

use map_macro::hash_map;

use crate::shared::io::read_lines_from_file;

/**
 * The first time I wrote this, I used regex to parse the instructions...
 * this took some 800s. After doing a basic split, the runtime is 141ms...
 * Let that be a lesson about when and when not to use regex :laughing:
 */
pub fn run() {
    let lines = read_lines_from_file("src/days/_12/input.txt");

    let mut registers: HashMap<&str, i32> = hash_map! {
        "a" => 0,
        "b" => 0,
        "c" => 0,
        "d" => 0
    };

    let mut line_num: usize = 0;

    while i < 40 && line_num < lines.len() {
        let line = lines.get(line_num).unwrap();
        let parts: Vec<&str> = line.split(" ").collect();

        // Crop reg -> reg
        if parts[0] == "cpy" {
            let from = parts[1];
            let to = parts[2];

            if let Some(val) = registers.get(from) {
                registers.insert(to, *val);
            } else {
                registers.insert(to, from.parse().unwrap());
            }

            line_num += 1;
            continue;
        }

        // Inc reg
        if parts[0] == "inc" {
            let reg = parts[1];

            registers.insert(reg, registers[reg]+1);
            line_num += 1;
            continue;
        }

        // Dec reg
        if parts[0] == "dec" {
            let reg = parts[1];

            registers.insert(reg, registers[reg]-1);
            line_num += 1;
            continue;
        }

        // Jump if reg not zero
        if parts[0] == "jnz" {
            let from = parts[1];
            let jmp: i32 = parts[2].parse().unwrap();

            let val = if let Some(reg_val) = registers.get(from) {
                *reg_val
            } else {
                from.parse().unwrap()
            };

            if val == 0 {
                line_num += 1;
            } else if jmp < 0 {
                line_num -= jmp.abs() as usize;
            } else {
                line_num += jmp as usize;
            }
            continue;
        }

        panic!("Unmatched instruction");
    }

    println!("Value of a: {}", registers["a"]);
}