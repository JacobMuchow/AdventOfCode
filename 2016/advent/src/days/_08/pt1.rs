#![allow(dead_code)]

use crate::shared::io::read_lines_from_file;
use regex::Regex;

fn print_grid(grid: &Vec<Vec<char>>) {
    for row in grid {
        // println!("{:?}", row);
        for c in row {
            print!("{}", c);
        }
        println!();
    }
    println!();
}

pub fn run() {
    let lines = read_lines_from_file("src/days/_08/input.txt");
    
    // Initialize grid with empty lights.
    // let grid_w = 7;
    // let grid_h = 3;
    let grid_w = 50;
    let grid_h = 6;
    let mut grid: Vec<Vec<char>> = Vec::with_capacity(grid_h);

    for _ in 0..grid_h {
        let mut row: Vec<char> = Vec::with_capacity(grid_w);
        for _ in 0..grid_w {
            row.push('.');
        }
        grid.push(row);
    }

    print_grid(&grid);
    
    for line in lines {
        // "rect WxH" instruction
        let re = Regex::new(r"rect ([0-9]+)x([0-9]+)").unwrap();
        if let Some(caps) = re.captures(&line) {
            let w: usize = caps.get(1).unwrap().as_str().parse().unwrap();
            let h: usize = caps.get(2).unwrap().as_str().parse().unwrap();

            for y in 0..h {
                for x in 0..w {
                    grid[y][x] = '#';
                }
            }

            continue;
        }

        // "rotate row y=A by B" instruction
        let re = Regex::new(r"rotate row y=([0-9]+) by ([0-9]+)").unwrap();
        if let Some(caps) = re.captures(&line) {
            let y: usize = caps.get(1).unwrap().as_str().parse().unwrap();
            let shift: usize = caps.get(2).unwrap().as_str().parse().unwrap();

            let mut new_row = Vec::clone(&grid[y]);

            for x in 0..grid_w {
                let new_x = (x + shift) % grid_w;
                new_row[new_x] = grid[y][x];
            }

            grid[y] = new_row;
            continue;
        }

        // "rotate column x=A by B" instruction
        let re = Regex::new(r"rotate column x=([0-9]+) by ([0-9]+)").unwrap();
        if let Some(caps) = re.captures(&line) {
            let x: usize = caps.get(1).unwrap().as_str().parse().unwrap();
            let shift: usize = caps.get(2).unwrap().as_str().parse().unwrap();

            // Create a temporary vec to hold the output.
            let mut new_col: Vec<char> = vec!['.'; grid_w];

            for y in 0..grid_h {
                let new_y = (y + shift) % grid_h;
                new_col[new_y] = grid[y][x];
            }

            // Copy the output vec into the grid.
            for y in 0..grid_h {
                grid[y][x] = new_col[y];
            }
            continue;
        }

        panic!("Unknown instruction: '{}'", line);
    }

    print_grid(&grid);

    // Count number of pixels.
    let mut count: u32 = 0;
    for row in grid {
        for c in row {
            if c == '#' {
                count += 1;
            }
        }
    }

    println!("Number lit: {}", count);
}