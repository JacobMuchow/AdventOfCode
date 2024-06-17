#![allow(dead_code)]

use std::collections::HashMap;
use regex::Regex;

use crate::shared::io::read_lines_from_file;
use crate::days::_10::models::*;

fn get_or_create_bot<'a>(bots: &'a mut HashMap<u32, Bot>, bot_id: u32) -> &'a mut Bot {
    bots.entry(bot_id).or_insert_with(|| Bot::new(bot_id))
}

pub fn run() {
    // I feel the challenge is not entirely descriptive, so before I being programming a solution, I am going to 
    // check for some things on the input:
    //  - Can a bot be initialized with more than 1 or 2 values?
    //  - Can a bot receive more than one "gives" instruction? My expectation is only 1.
    //  - Are the lines instructions like a program, i.e. execute in exact order, or should I read all instructions
    //      to "initialize" the system then process states like a queue? I think it is the latter.
    //  - In this case, does the processing order matter? Or does it happen to not matter because of the nature
    //      of the mappings?

    let mut bots: HashMap<u32, Bot> = HashMap::new();
    let mut output_bins: HashMap<u32, OutputBin> = HashMap::new();

    let lines = read_lines_from_file("src/days/_10/test.txt");
    for line in lines {
        println!("{}", line);

        let re = Regex::new(r"^value ([0-9]+) goes to bot ([0-9]+)").unwrap();
        if let Some(caps) = re.captures(&line) {
            let bot_id: u32 = caps.get(2).unwrap().as_str().parse().unwrap();
            let chip_num: u32 = caps.get(1).unwrap().as_str().parse().unwrap();

            let bot = get_or_create_bot(&mut bots, bot_id);
            bot.chips.push(chip_num);
            continue;
        }

        let re = Regex::new(r"^bot ([0-9]+) gives low to (bot|output) ([0-9]+) and high to (bot|output) ([0-9]+)").unwrap();
        if let Some(caps) = re.captures(&line) {
            let bot_id: u32  = caps.get(1).unwrap().as_str().parse().unwrap();
            let low_type     = caps.get(2).unwrap().as_str();
            let low_id: u32  = caps.get(3).unwrap().as_str().parse().unwrap();
            let high_type    = caps.get(4).unwrap().as_str();
            let high_id: u32 = caps.get(5).unwrap().as_str().parse().unwrap();
            
            let bot = get_or_create_bot(&mut bots, bot_id);

            let low_target: Target = if low_type == "bot" { Target::Bot(low_id) } else { Target::OutputBin(low_id) };
            let high_target = if high_type == "bot" { Target::Bot(high_id) } else { Target::OutputBin(high_id) };

            bot.gives = Some((low_target, high_target));
            continue;
        }

        panic!("Failed to match line {}", line);
    }

    println!("{:#?}", bots);
}