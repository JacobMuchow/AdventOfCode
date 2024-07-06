#![allow(dead_code)]

use std::collections::HashMap;

use crate::shared::io::read_lines_from_file;

type Pos2d = (usize, usize);

fn is_wall(pos: &Pos2d, fave_num: usize, wall_cache: &mut HashMap<String, bool>) -> bool {
    let cache_key = key_for(pos);
    if let Some(is_wall) = wall_cache.get(&cache_key) {
        return *is_wall
    }

    let (x, y) = pos;
    let sum = (x*x) + (3*x) + (2*x*y) + y + (y*y) + fave_num;
    let binary = format!("{:b}", sum);

    let mut count = 0;
    for c in binary.chars() {
        if c == '1' {
            count += 1;
        }
    }

    let is_wall = count % 2 == 1;
    wall_cache.insert(cache_key, is_wall);
    is_wall
}

fn key_for((x, y): &Pos2d) -> String {
    format!("{},{}", x, y)
}

fn should_visit(pos: &Pos2d, wall_cache: &mut HashMap<String, bool>, fave_num: usize, visited: &HashMap<String, usize>, dist: usize) -> bool {
    if is_wall(pos, fave_num, wall_cache) {
        return false;
    }

    match visited.get(&key_for(pos)) {
        None => true,
        Some(val) => dist < *val
    }
}

pub fn run() {
    let fave_num: usize = 10;
    let goal_x = 7;
    let goal_y = 4;

    let mut wall_cache: HashMap<String, bool> = HashMap::new();
    let mut visited: HashMap<String, usize> = HashMap::new();
    let mut path: Vec<(usize, usize)> = Vec::from([(1, 1)]);
    let mut best_dist = usize::MAX;

    while !path.is_empty() {
        let pos = path.last().unwrap();
        let (x, y) = pos;
        
        println!("q: {},{}", x, y);

        visited.insert(key_for(pos), path.len());
        
        // Gone past best dist, no need to continue.
        if path.len() >= best_dist {
            path.pop();
            continue;
        }

        // Check if goal state
        if x == &goal_x && y == &goal_y {
            best_dist = path.len();
            path.pop();
            continue;
        }

        // Test next cardinal direction that is unvisited (or new path is more optimal).

        // Right
        if *x < usize::MAX {
            let next: Pos2d = (*x+1, *y);
            if should_visit(&next, &mut wall_cache, fave_num, &visited, path.len()+1) {
                path.push(next);
                continue;
            }
        }

        // Down
        if *y < usize::MAX {
            let next: Pos2d = (*x, *y+1);
            if should_visit(&next, &mut wall_cache, fave_num, &visited, path.len()+1) {
                path.push(next);
                continue;
            }
        }

        // Left
        if *x > 0 {
            let next: Pos2d = (*x-1, *y);
            if should_visit(&next, &mut wall_cache, fave_num, &visited, path.len()+1) {
                path.push(next);
                continue;
            }
        }

        // Up
        if *y > 0 {
            let next: Pos2d = (*x, *y-1);
            if should_visit(&next, &mut wall_cache, fave_num, &visited, path.len()+1) {
                path.push(next);
                continue;
            }
        }

        path.pop();
    }

    println!("Best dist to goal: {}", best_dist-1);
}