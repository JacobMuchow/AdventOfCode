#![allow(dead_code)]

use std::collections::{BTreeSet, HashMap, VecDeque};

use map_macro::btree_set;

// use crate::shared::io::read_lines_from_file;
use crate::days::_11::models::*;

fn key_for_state(state: &GameState) -> String {
    format!("{:?}", state)
}

fn state_is_valid(state: &GameState) -> bool {
    for floor in &state.floors {
        'items_outer: for item in floor {
            match item {
                Item::Microchip(el) => {
                    let mut chip_unsafe = false;

                    // Check generators on the floor to see if the chip is safe or not.
                    for item2 in floor {
                        match item2 {
                            Item::Generator(el2) => {
                                // If a genereator with matching element is found,
                                // this chip is safe and we can continue checking items.
                                if el == el2 {
                                    continue 'items_outer
                                }

                                // Otherwise, the chip may be unsafe unless we do find a matching
                                // generator in this list.
                                chip_unsafe = true;
                            },
                            _ => continue
                        }
                    }

                    // No matching generator was found, so this chip is unsafe and the state if invalid.
                    if chip_unsafe {
                        return false;
                    }
                },
                _ => continue 'items_outer
            }
        }
    }

    // If we've reached this point, then there are no floors with unprotected chips
    // so the state is valid.
    return true;
}

pub fn run() {
    let floors: Vec::<BTreeSet::<Item>> = vec![
        btree_set! { Item::Microchip(Element::Hydrogen), Item::Microchip(Element::Lithium) },
        btree_set! { Item::Generator(Element::Hydrogen) },
        btree_set! { Item::Generator(Element::Lithium) },
        btree_set! {}
    ];
    let num_items: usize = 4;
    let num_floors: usize = floors.len();

    let state = GameState {
        floors,
        cur_floor: 0
    };

    let valid = state_is_valid(&state);
    println!("Origin state valid: {}", valid);
    return;

    let mut queue = VecDeque::<(GameState, i8)>::from([(state, 0)]);
    let mut visited = HashMap::<String, i8>::new();
    let mut min_moves = i8::MAX;
    let mut i = 0;

    while !queue.is_empty() {
        let (state, num_moves) = queue.pop_front().unwrap();

        println!("qi {}: {:?}", i, state);
        i += 1;

        // This path has exceeded current known min, no need to continue.
        if num_moves >= min_moves {
            continue;
        }

        // If this state has already been visited w/ less moves, then ignore.
        if let Some(prev_moves) = visited.get(&key_for_state(&state)) {
            if prev_moves <= &num_moves {
                continue;
            }
        }
        visited.insert(key_for_state(&state), num_moves);

        // If we are in the "win" state, then set min num moves.
        if state.floors.get(num_floors-1).unwrap().len() == num_items {
            min_moves = num_moves;
            continue;
        }

        // Finally check state validity and toss it if invalid.

        let cur_floor = state.floors.get(state.cur_floor).unwrap();

        for item in cur_floor {
            // We will enqueue some different states to try... first we will remove item from cur floor.
            let mut state = state.clone();
            state.floors.get_mut(state.cur_floor).unwrap().remove(item);

            // Queue move up
            if state.cur_floor < num_floors-1 {
                let mut new_state = state.clone();
                new_state.cur_floor += 1;
                new_state.floors.get_mut(state.cur_floor+1).unwrap().insert(item.clone());

                queue.push_back((new_state, num_moves+1));
            }

            // Queue move down
            if state.cur_floor > 0 {
                let mut new_state = state.clone();
                new_state.cur_floor -= 1;
                new_state.floors.get_mut(state.cur_floor-1).unwrap().insert(item.clone());

                queue.push_back((new_state, num_moves+1));
            }

            // Now we will try moving pairs (TODO)
        }
    }

    
}