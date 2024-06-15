use std::{collections::HashMap, fmt, fs::read_to_string};
use regex::Regex;

enum Direction {
    North,
    East,
    South,
    West
}

impl Direction {
    fn right(&self) -> Direction {
        match self {
            North => East,
            East => South,
            South => West,
            West => North
        }
    }
    fn left(&self) -> Direction {
        match self {
            North => West,
            West => South,
            South => East,
            East => North
        }
    }
}

use Direction::*;

fn read_lines(path: &str) -> Vec<String> {
    read_to_string(path)
        .unwrap()
        .lines()
        .map(String::from)
        .collect()
}

pub fn run() {
    let lines = read_lines("src/days/_01/input.txt");
    let line = lines.get(0).unwrap();

    // Parse directions
    let re = Regex::new(r"([LR])([0-9]+)").unwrap();
    let directions = re.captures_iter(line.as_str()).map(|caps| {
        let dir = caps.get(1).map(|m| m.as_str()).unwrap();
        let dist = caps.get(2).map(|m| m.as_str().parse::<i32>().unwrap()).unwrap();
        (dir, dist)
    });

    // Initialize position & direction
    let mut x = 0_i32;
    let mut y = 0_i32;
    let mut facing = North;
    let mut visited: HashMap<String, bool> = HashMap::new();
    visited.insert(String::from("0,0"), true);

    // Handle all directions
    'outer: for (dir, dist) in directions {
        // Turn to new direction.
        if dir == "R" {
            facing = facing.right();
        } else if dir == "L" {
            facing = facing.left();
        } else {
            panic!("Unexpected dir: '{}'", dir);
        }

        for _ in 0..dist {
            // Move forward
            match facing {
                North => y += 1,
                South => y -= 1,
                East => x += 1,
                West => x -= 1,
            }
    
            let key = format!("{},{}", x, y);
            if visited.contains_key(key.as_str()) {
                break 'outer;
            }
            visited.insert(key, true);
        }
    }

    println!("Final pos: {}, {}", x, y);

    let shortest_path = x.abs() + y.abs();
    println!("Shortest path: {}", shortest_path);
}