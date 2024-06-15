#![allow(dead_code)]

use crate::shared::io::read_lines_from_file;
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

pub fn run() {
    let lines = read_lines_from_file("src/days/_01/input.txt");
    let line = lines.get(0).unwrap();

    // Parse directions
    let re = Regex::new(r"([LR])([0-9]+)").unwrap();
    let directions = re.captures_iter(line.as_str()).map(|caps| {
        let dir = caps.get(1).map(|m| m.as_str()).unwrap();
        let dist = caps.get(2).map(|m| m.as_str().parse::<i32>().unwrap()).unwrap();
        (dir, dist)
    });

    // Initialize position & direction
    let mut x = 0;
    let mut y = 0;
    let mut facing = North;

    // Handle all directions
    for (dir, dist) in directions {
        // Turn to new direction.
        if dir == "R" {
            facing = facing.right();
        } else if dir == "L" {
            facing = facing.left();
        } else {
            panic!("Unexpected dir: '{}'", dir);
        }

        // Move forward
        match facing {
            North => y += dist,
            South => y -= dist,
            East => x += dist,
            West => x -= dist,
        }
    }

    println!("Final pos: {}, {}", x, y);

    let shortest_path = x.abs() + y.abs();
    println!("Shortest path: {}", shortest_path);
}