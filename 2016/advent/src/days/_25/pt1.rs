#![allow(dead_code)]

use std::collections::HashMap;

use map_macro::hash_map;

use crate::shared::io::read_lines_from_file;

fn is_reg(reg: &str) -> bool {
    reg == "a" || reg == "b" || reg == "c" || reg == "d"
}

fn get_reg_or_parse(val: &str, registers: &HashMap<String, i32>) -> i32 {
    if is_reg(val) {
        return registers[val];
    } else {
        return val.parse().unwrap();
    }
}

fn run_program(lines: &Vec<String>, a: i32) -> bool {
    let mut lines = lines.clone();
    let mut registers: HashMap<String, i32> = hash_map! {
        String::from("a") => a,
        String::from("b") => 0,
        String::from("c") => 0,
        String::from("d") => 0
    };

    let mut line_num: usize = 0;
    let mut i = 0_u32;

    let mut expected_signal = 0_i32;
    let mut signal_count = 0_u32;

    while line_num < lines.len() {
        let line = String::from(lines.get(line_num).unwrap());
        let parts: Vec<&str> = line.split(" ").collect();

        // if i % 100000 == 0 {
        //     println!("Registers: {:?}", registers);
        //     println!("Line {}: {}", line_num, line);
        // }
        // i += 1;

        // Optimizing these lines.
        // L1-7 --> d += 365 * 7
        if line_num == 1 {
            registers.insert(String::from("d"), registers["d"] + (365 * 7));
            registers.insert(String::from("b"), 0);
            registers.insert(String::from("c"), 0);

            line_num += 7;
            continue;
        }

        if parts[0] == "out" {
            let val = get_reg_or_parse(parts[1], &registers);
            if val != expected_signal {
                return false;
            }

            // Break after 100 repeats.
            if signal_count == 100 {
                return true;
            }
            signal_count += 1;

            expected_signal = if expected_signal == 0 { 1 } else { 0 };

            line_num += 1;
            continue;
        }

        // Toggle instruction
        if parts[0] == "tgl" {
            let jmp = get_reg_or_parse(parts[1], &registers);

            let mut new_line = line_num;

            // Get line number for instruction to toggle.
            if jmp < 0 {
                // Make sure we don't go out of bounds.
                if jmp.abs() as usize > line_num {
                    line_num += 1;
                    continue;
                }
                new_line -= jmp.abs() as usize;
            } else {
                // Make sure we don't go out of bounds.
                if (line_num + jmp as usize) >= lines.len() {
                    line_num += 1;
                    continue;
                }
                new_line += jmp as usize;
            }

            let ins = lines.get(new_line).unwrap();
            let ins_parts: Vec<&str> = ins.split(" ").collect();
            let mut new_lines = lines.clone();

            if ins_parts.len() == 2 {
                if ins_parts[0] == "inc" {
                    new_lines[new_line] = format!("dec {}", ins_parts[1]);
                } else {
                    new_lines[new_line] = format!("inc {}", ins_parts[1]);
                }
            } else if ins_parts.len() == 3 {
                if ins_parts[0] == "jnz" {
                    new_lines[new_line] = format!("cpy {} {}", ins_parts[1], ins_parts[2]);
                } else {
                    new_lines[new_line] = format!("jnz {} {}", ins_parts[1], ins_parts[2]);
                }
            }

            lines = new_lines;
            line_num += 1;
            continue;
        }

        // Copy reg -> reg
        if parts[0] == "cpy" {
            let val = get_reg_or_parse(parts[1], &registers);
            let to_reg = parts[2];

            // Can only copy to reg.
            if !is_reg(to_reg) {
                line_num += 1;
                continue;
            }

            registers.insert(String::from(to_reg), val);

            line_num += 1;
            continue;
        }

        // Inc reg
        if parts[0] == "inc" {
            let reg = parts[1];

            registers.insert(String::from(reg), registers[reg] + 1);
            line_num += 1;
            continue;
        }

        // Dec reg
        if parts[0] == "dec" {
            let reg = parts[1];

            registers.insert(String::from(reg), registers[reg] - 1);
            line_num += 1;
            continue;
        }

        // Jump if reg not zero
        if parts[0] == "jnz" {
            let flag = get_reg_or_parse(parts[1], &registers);
            let jmp = get_reg_or_parse(parts[2], &registers);

            if flag == 0 {
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

    println!("Program ended unexpectedly.");
    return false;
}

/**
 * Copied initial code from day 12.
 */
pub fn run() {
    let lines = read_lines_from_file("src/days/_25/input.txt");

    let mut a = 0_i32;

    loop {
        println!("Testing a = {}", a);
        let valid = run_program(&lines, a);
        if valid {
            break;
        }
        a += 1;
    }

    println!("Solution found: {}", a);
}
