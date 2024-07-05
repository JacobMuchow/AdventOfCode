#![allow(dead_code)]

use crate::shared::io::read_lines_from_file;

fn is_wall(x: usize, y: usize, fave_num: usize) -> bool {
    let sum = (x*x) + (3*x) + (2*x*y) + y + (y*y) + fave_num;
    let binary = format!("{:b}", sum);

    let mut count = 0;
    for c in binary.chars() {
        if c == '1' {
            count += 1;
        }
    }

    count % 2 == 1
}

pub fn run() {
    let fave_num: usize = 10;
    let mut grid: Vec<Vec<char>> = vec![vec!['.'; 10]; 10];

    for y in 0..grid.len() {
        for x in 0..grid[0].len() {
            grid[y][x] = if is_wall(x, y, fave_num) {
                '#'
            } else {
                '.'
            }
        }
    }

    for y in 0..grid.len() {
        for x in 0..grid[0].len() {
            print!("{}", grid[y][x]);
        }
        println!();
    }
}