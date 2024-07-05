#![allow(dead_code)]

use std::collections::HashMap;

use map_macro::hash_map;
use regex::Regex;

use crate::shared::io::read_lines_from_file;

pub fn run() {
    let lines = read_lines_from_file("src/days/_12/input.txt");

    let mut registers: HashMap<&str, i32> = hash_map! {
        "a" => 0,
        "b" => 0,
        "c" => 0,
        "d" => 0
    };

    let mut line_num: usize = 0;
    let mut i = 0;

    while i < 40 && line_num < lines.len() {
        // i += 1;
        let line = lines.get(line_num).unwrap();
        // println!("{:?}", registers);
        // println!("l{}: {}\n", line_num, line);

        // Crop reg -> reg
        let re = Regex::new(r"cpy ([+-]?[a-d0-9]+) ([a-d])").unwrap();
        if let Some(caps) = re.captures(line) {
            let from = caps.get(1).unwrap().as_str();
            let to = caps.get(2).unwrap().as_str();

            if let Some(val) = registers.get(from) {
                registers.insert(to, *val);
            } else {
                registers.insert(to, from.parse().unwrap());
            }

            line_num += 1;
            continue;
        }

        // Inc reg
        let re = Regex::new(r"inc ([a-d])").unwrap();
        if let Some(caps) = re.captures(line) {
            let reg = caps.get(1).unwrap().as_str();

            registers.insert(reg, registers[reg]+1);
            line_num += 1;
            continue;
        }

        // Dec reg
        let re = Regex::new(r"dec ([a-d])").unwrap();
        if let Some(caps) = re.captures(line) {
            let reg = caps.get(1).unwrap().as_str();

            registers.insert(reg, registers[reg]-1);
            line_num += 1;
            continue;
        }

        // Jump if reg not zero
        let re = Regex::new(r"jnz ([+-]?[a-d0-9]+) ([+-]?[0-9]+)").unwrap();
        if let Some(caps) = re.captures(line) {
            let from = caps.get(1).unwrap().as_str();
            let jmp: i32 = caps.get(2).unwrap().as_str().parse().unwrap();

            let val = if let Some(reg_val) = registers.get(from) {
                *reg_val
            } else {
                from.parse().unwrap()
            };

            // println!("val: {}", val);

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