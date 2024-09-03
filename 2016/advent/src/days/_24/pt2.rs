#![allow(dead_code)]

use std::{
    collections::{HashMap, HashSet, VecDeque},
    u32,
};

use map_macro::{hash_map, hash_set, vec_deque};

use crate::shared::io::read_lines_from_file;

type Grid = Vec<Vec<char>>;
type Hotspots = HashMap<char, Pos2d>;
type Pos2d = (usize, usize);

#[derive(Clone)]
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

// From some "hotspot" (x, y), find the next N possible hotspots that can be navigated to.
fn next_possible_spots(state: &MapState) -> Vec<(Pos2d, u32)> {
    let mut spots = Vec::<(Pos2d, u32)>::new();

    let mut visited: HashSet<Pos2d> = hash_set! {};
    let mut queue: VecDeque<(Pos2d, u32)> = vec_deque![(state.pos, 0)];

    while !queue.is_empty() {
        let (pos, steps) = queue.pop_front().unwrap();
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
            spots.push((pos, steps));
            continue;
        }

        // This is a empty space, so we must enqueue next possible options.
        if x > 0 {
            queue.push_back(((x - 1, y), steps + 1));
        }
        if x < state.grid[0].len() {
            queue.push_back(((x + 1, y), steps + 1));
        }
        if y > 0 {
            queue.push_back(((x, y - 1), steps + 1));
        }
        if y < state.grid.len() {
            queue.push_back(((x, y + 1), steps + 1));
        }
    }

    return spots;
}

// Enqueue next map state in sorted order, priotize states with least # of steps.
fn priority_enqueue(queue: &mut VecDeque<MapState>, new_state: MapState) {
    for i in 0..queue.len() {
        if new_state.num_steps <= queue[i].num_steps {
            queue.insert(i, new_state);
            return;
        }
    }

    queue.push_back(new_state);
}

// For pt 2, all that needed to be done is add this function to be called at the end, after hitting all spots,
// to calculate the #steps to return to start.
fn dis_to_start(state: &MapState, start_pos: Pos2d) -> u32 {
    let mut min_dis = u32::MAX;

    let mut visited: HashMap<Pos2d, u32> = hash_map! {};
    let mut queue: VecDeque<(Pos2d, u32)> = vec_deque![(state.pos, 0)];

    while !queue.is_empty() {
        let (pos, steps) = queue.pop_front().unwrap();

        // Exceeded best soln so far.
        if steps >= min_dis {
            continue;
        }

        // Ignore walls.
        if state.grid[pos.1][pos.0] == '#' {
            continue;
        }

        // New solution found!
        if pos == start_pos {
            min_dis = steps;
            continue;
        }

        // If we've visited this space before in les steps, ignore.
        if let Some(prev_steps) = visited.get(&pos) {
            if steps >= *prev_steps {
                continue;
            }
        }
        visited.insert(pos, steps);

        // Enqueue next options.
        let (x, y) = pos;
        if x > 0 {
            queue.push_back(((x - 1, y), steps + 1));
        }
        if x < state.grid[0].len() {
            queue.push_back(((x + 1, y), steps + 1));
        }
        if y > 0 {
            queue.push_back(((x, y - 1), steps + 1));
        }
        if y < state.grid.len() {
            queue.push_back(((x, y + 1), steps + 1));
        }
    }

    min_dis
}

/**
 * These solutions work, albeit a bit slowly (pt1: 3.5s, pt2: 18.8s).
 * I think this could be improved dramatically using Djikstra's algorithm,
 * but luckily the problems are small enough that a crude solution works well enough.
 */
pub fn run() {
    // Parse grid input
    let mut grid = parse_input("src/days/_24/input.txt");
    print_grid(&grid);

    // Find the "hotspot" locations & start pos.
    let mut hotspots = get_hotspots(&grid);
    let start_pos = hotspots[&'0'];
    hotspots.remove(&'0');

    println!("Hotspots: {:?}", hotspots);
    println!("Starting at {:?}", start_pos);

    // Mark this spot as "clean" automatically so our algo will work.
    grid[start_pos.1][start_pos.0] = '.';

    let state = MapState {
        grid,
        hotspots,
        pos: start_pos,
        num_steps: 0,
    };

    let mut queue = vec_deque![state];
    let mut min_steps = u32::MAX;

    // Priority DFS queue to find solution.
    while !queue.is_empty() {
        let state = queue.pop_front().unwrap();

        // Exceeded best solution so far, no need to continue.
        if state.num_steps >= min_steps {
            continue;
        }

        // There are no hotspots left, this is a new potential solution!
        if state.hotspots.is_empty() {
            let final_steps = dis_to_start(&state, start_pos);
            min_steps = min_steps.min(state.num_steps + final_steps);
            continue;
        }

        // Otherwise, look for next possible spots to clean and enqueue those states.
        let next_spots = next_possible_spots(&state);
        for (next, steps) in next_spots {
            let mut new_state = state.clone();

            // Mark spot as cleaned & set up next state.
            let symbol = new_state.grid[next.1][next.0];
            new_state.grid[next.1][next.0] = '.';
            new_state.hotspots.remove(&symbol);
            new_state.pos = next;
            new_state.num_steps += steps;

            // Enqueue new state
            priority_enqueue(&mut queue, new_state);
        }
    }

    println!("Solution: {}", min_steps);
}
