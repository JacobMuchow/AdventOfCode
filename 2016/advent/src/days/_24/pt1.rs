#![allow(dead_code)]

use std::collections::HashMap;

use crate::shared::io::read_lines_from_file;

type Grid = Vec<Vec<char>>;
type Pos2d = (usize, usize);

fn parse_input(filename: &str) -> Grid {
    let lines = read_lines_from_file(filename);
    return lines.iter().map(|line| line.chars().collect()).collect();
}

fn get_hotspots(grid: &Grid) -> HashMap<char, Pos2d> {
    let mut hotspots = HashMap::new();

    for (y, row) in grid.iter().enumerate() {
        for (x, cell) in row.iter().enumerate() {
            if cell.is_digit(10) {
                hotspots.insert(*cell, (x, y));
            }
        }
    }

    return hotspots;
}

fn print_grid(grid: &Grid) {
    for row in grid {
        for cell in row {
            print!("{}", cell);
        }
        println!();
    }
}

pub fn run() {
    let grid = parse_input("src/days/_24/input.txt");
    print_grid(&grid);

    let hotspots = get_hotspots(&grid);
    let digits = hotspots.keys().collect::<Vec<&char>>();

    println!("Hotspots: {:?}", hotspots);
    println!("Digits: {:?}", digits);

    let mut unvisited = digits.clone();
    let mut pos = hotspots[&'0'];

    println!("Starting at {:?}", pos);
}
