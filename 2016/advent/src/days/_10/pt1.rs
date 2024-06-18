#![allow(dead_code)]

use std::collections::{HashMap, VecDeque};
use regex::Regex;

use crate::shared::io::read_lines_from_file;
use crate::days::_10::models::*;

fn get_or_create_bot<'a>(bots: &'a mut HashMap<u32, Bot>, bot_id: u32) -> &'a mut Bot {
    bots.entry(bot_id).or_insert_with(|| Bot::new(bot_id))
}

fn get_or_create_output_bin<'a>(bins: &'a mut HashMap<u32, OutputBin>, bin_id: u32) -> &'a mut OutputBin {
    bins.entry(bin_id).or_insert_with(|| OutputBin::new(bin_id))
}

fn get_or_create_target<'a>(bots: &'a mut HashMap<u32, Bot>, output_bins: &'a mut HashMap<u32, OutputBin>, target_type: &String, target_id: u32) -> Target {
    if target_type == "box" {
        get_or_create_bot(bots, target_id);
        Target::Bot(target_id)
    } else {
        get_or_create_output_bin(output_bins, target_id);
        Target::OutputBin(target_id)
    }
}

pub fn run() {
    // I feel the challenge is not entirely descriptive, so before I being programming a solution, I am going to 
    // check for some things on the input:
    //  - Can a bot be initialized with more than 1 or 2 values?
    //      - Answer: no.
    //  - Can a bot receive more than one "gives" instruction? My expectation is only 1.
    //      - Answer: no.
    //  - Are the lines instructions like a program, i.e. execute in exact order, or should I read all instructions
    //      to "initialize" the system then process states like a queue? I think it is the latter.
    //      - In this case, does the processing order matter? Or does it happen to not matter because of the nature
    //      of the mappings.
    //      - Answer: no. only 1 bot is initialized with 2 chips.

    
    // Not particularly proud of the final code here in terms of the amount of code I needed to write.
    //  I know it would be simpler in other languages and I feel there must be a shorter way to write it in Rust.
    //  I feel my grasp on Rust memory management is not so strong yet, but this does get the job done.

    let mut bots: HashMap<u32, Bot> = HashMap::new();
    let mut output_bins: HashMap<u32, OutputBin> = HashMap::new();

    let lines = read_lines_from_file("src/days/_10/input.txt");
    for line in lines {
        // Parse value initialization line.
        let re = Regex::new(r"^value ([0-9]+) goes to bot ([0-9]+)").unwrap();
        if let Some(caps) = re.captures(&line) {
            let bot_id: u32 = caps.get(2).unwrap().as_str().parse().unwrap();
            let chip_num: u32 = caps.get(1).unwrap().as_str().parse().unwrap();

            let bot = get_or_create_bot(&mut bots, bot_id);
            bot.chips.push(chip_num);
            continue;
        }

        // Parse gives instructions line.
        let re = Regex::new(r"^bot ([0-9]+) gives low to (bot|output) ([0-9]+) and high to (bot|output) ([0-9]+)").unwrap();
        if let Some(caps) = re.captures(&line) {
            let bot_id: u32  = caps.get(1).unwrap().as_str().parse().unwrap();
            let low_type     = caps.get(2).unwrap().as_str();
            let low_id: u32  = caps.get(3).unwrap().as_str().parse().unwrap();
            let high_type    = caps.get(4).unwrap().as_str();
            let high_id: u32 = caps.get(5).unwrap().as_str().parse().unwrap();
            
            let bot = get_or_create_bot(&mut bots, bot_id);
            if bot.gives.is_some() {
                panic!("Bot {} already has gives instruction!", bot.id);
            }

            let low_target: Target = if low_type == "bot" { Target::Bot(low_id) } else { Target::OutputBin(low_id) };
            let high_target = if high_type == "bot" { Target::Bot(high_id) } else { Target::OutputBin(high_id) };

            bot.gives = Some((low_target, high_target));
            continue;
        }

        panic!("Failed to match line {}", line);
    }

    // Let's treat this like a queue problem, where for any step there are N bots
    // with 2 chips, meaning they need to follow their gives command.
    let mut queue: VecDeque<u32> = VecDeque::new();

    for bot in bots.values() {
        if bot.chips.len() > 2 {
            println!("Bot {} has {} chips. This is unexpected!", bot.id, bot.chips.len());
        } else if bot.chips.len() == 2 {
            queue.push_back(bot.id);
        }
    }

    while !queue.is_empty() {
        let bot_id = queue.pop_front().unwrap();

        // I created the get_or_create() functions to try to make the code simpler, but it involves
        // to use them again later I need the "bot" we grab here to only live for a certain scope. 
        // So we will extract the values we need to these variables then proceed.
        let low_val: u32;
        let high_val: u32;
        let low_target: Target;
        let high_target: Target;

        {
            let bot = get_or_create_bot(&mut bots, bot_id);
            low_val = bot.chips[0].min(bot.chips[1]);
            high_val = bot.chips[0].max(bot.chips[1]);

            // No need to continue processing the queue, we can print & break at this point since this is
            // what the question asks for.
            if low_val == 17 && high_val == 61 {
                println!("Bot {} is responsible for 17 & 61.", bot_id);
                break;
            }

            bot.chips.clear();

            let gives = bot.gives.as_ref().unwrap().clone();
            low_target = gives.0;
            high_target = gives.1;
        }

        // Send low value to corresponding target.
        match low_target {
            Target::Bot(id) => {
                let bot = get_or_create_bot(&mut bots, id);
                bot.chips.push(low_val);
                if bot.chips.len() == 2 {
                    queue.push_back(bot.id);
                }
            },
            Target::OutputBin(id) => get_or_create_output_bin(&mut output_bins, id).chips.push(low_val),
        }

        // Send high value to corresponding target.
        match high_target {
            Target::Bot(id) =>  {
                let bot = get_or_create_bot(&mut bots, id);
                bot.chips.push(high_val);
                if bot.chips.len() == 2 {
                    queue.push_back(bot.id);
                }
            },
            Target::OutputBin(id) => get_or_create_output_bin(&mut output_bins, id).chips.push(high_val),
        }
    }

    // println!("Queue complete.");
    // println!("");
    // println!("Bots: {:#?}", bots);
    // println!("");
    // println!("Output bins: {:#?}", output_bins);
    // println!("");
}