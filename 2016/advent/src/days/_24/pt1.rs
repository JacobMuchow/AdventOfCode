#![allow(dead_code)]

use std::collections::{HashMap, HashSet, VecDeque};

use map_macro::{hash_set, vec_deque};

use crate::{days::_11::models::GameState, shared::io::read_lines_from_file};

type Grid = Vec<Vec<char>>;
type Hotspots = HashMap<char, Pos2d>;
type Pos2d = (usize, usize);

struct MapState {
    grid: Grid,
    hotspots: Hotspots,
    pos: Pos2d,
    num_steps: u32,
}

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

fn next_possible_spots(state: &MapState) -> Vec<Pos2d> {
    let mut spots = Vec::<Pos2d>::new();

    let mut visited: HashSet<Pos2d> = hash_set! {};
    let mut queue: VecDeque<Pos2d> = vec_deque![state.pos];

    while !queue.is_empty() {
        let pos = queue.pop_front().unwrap();
        let (x, y) = pos;
        let symbol = state.grid[y][x];

        // Ignore walls
        if symbol == '#' {
            continue;
        }

        // Do not re-visit
        if visited.contains(&pos) {
            continue;
        }
        visited.insert(pos);

        // Found hot spot, add to viable options.
        if symbol.is_digit(10) {
            spots.push(pos);
            continue;
        }

        // This is a empty space, so we must enqueue next possible options.
        if x > 0 {
            queue.push_back((x - 1, y));
        }
        if x < state.grid[0].len() {
            queue.push_back((x + 1, y));
        }
        if y > 0 {
            queue.push_back((x, y - 1));
        }
        if y < state.grid.len() {
            queue.push_back((x, y + 1));
        }
    }

    return spots;
}

pub fn run() {
    let mut grid = parse_input("src/days/_24/test.txt");
    print_grid(&grid);

    let hotspots = get_hotspots(&grid);
    let total_hotspots = hotspots.len();
    println!("Hotspots: {:?}", hotspots);

    let mut pos = hotspots[&'3'];

    println!("Starting at {:?}", pos);
    println!("Total: {}", total_hotspots);

    grid[pos.1][pos.0] = '.';

    let state = MapState {
        grid,
        hotspots,
        pos,
        num_steps: 0,
    };

    let next_spots = next_possible_spots(&state);
    println!("Next spots: {:?}", next_spots);
}
