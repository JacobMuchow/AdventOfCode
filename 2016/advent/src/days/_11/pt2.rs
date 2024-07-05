#![allow(dead_code)]

use std::collections::{BTreeSet, HashMap, VecDeque};

use map_macro::btree_set;

use crate::days::_11::models::*;

fn key_for_state(state: &GameState) -> String {
    let mut key = format!("{}", state.cur_floor);

    for floor in &state.floors {
        key += "F|";

        let mut count_pairs = 0;
        let mut count_gen = 0;
        let mut count_chip = 0;

        for item in floor.iter() {
            match item {
                Item::Microchip(el) => {
                    // Check generators on the floor to see if the chip has a pair
                    let mut has_pair = false;
                    for item2 in floor {
                        match item2 {
                            Item::Generator(el2) => {
                                // If a genereator with matching element is found,
                                // this chip is safe and we can continue checking items.
                                if el == el2 {
                                    has_pair = true;
                                    break;
                                }
                            },
                            _ => continue
                        }
                    }

                    if has_pair {
                        count_pairs += 2;
                    } else {
                        count_chip += 1;
                    }
                },
                Item::Generator(el) => {
                    // Check generators on the floor to see if the chip has a pair
                    let mut has_pair = false;
                    for item2 in floor {
                        match item2 {
                            Item::Microchip(el2) => {
                                // If a genereator with matching element is found,
                                // this chip is safe and we can continue checking items.
                                if el == el2 {
                                    has_pair = true;
                                    break;
                                }
                            },
                            _ => continue
                        }
                    }

                    if has_pair {
                        count_pairs += 2;
                    } else {
                        count_gen += 1;
                    }
                },
            }

            key += &format!("P{}G{}C{}", count_pairs, count_gen, count_chip);
        }
    }

    key
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

fn move_floors(state: &GameState, item: &Item, from_floor_idx: usize, to_floor_idx: usize) -> Option<GameState> {
    let mut new_state = state.clone();

    if new_state.floors[from_floor_idx].remove(item) {
        new_state.floors[to_floor_idx].insert(item.clone());
        new_state.cur_floor = to_floor_idx;
        Some(new_state)
    } else {
        None
    }
}

/*
    Got pt2 working after adding an optimization to pt1 about how next steps
    are selected from some dequeued state.. this completes not but still takes 28s :grimace:

    Pt 2: Adds 4 more items to floor 1, so as expected this blew up (exponentially, factorially?).
    I tried some optimizations without too much luck, but gained a key insight from reddit
    about pairs being equivalent no matter the element, which becomes crucial for evaluating 
    visited states. With this knowledge, I rewrote my key function and took solution from 28s down to 786ms.
    Facepalm because I think I would have seen this if I thought about it more before going to reddit.
*/
pub fn run() {
    let floors: Vec::<BTreeSet::<Item>> = vec![
        btree_set! { Item::Generator(Element::Thulium), Item::Microchip(Element::Thulium), Item::Generator(Element::Plutonium), Item::Generator(Element::Strontium), Item::Generator(Element::Elerium), Item::Microchip(Element::Elerium), Item::Generator(Element::Dilithium), Item::Microchip(Element::Dilithium) },
        btree_set! { Item::Microchip(Element::Plutonium), Item::Microchip(Element::Strontium) },
        btree_set! { Item::Generator(Element::Promethium), Item::Microchip(Element::Promethium), Item::Generator(Element::Ruthenium), Item::Microchip(Element::Ruthenium) },
        btree_set! {}
    ];
    let num_items: usize = 14;  // too lazy to count this

    let num_floors: usize = floors.len();

    let state = GameState {
        floors,
        cur_floor: 0
    };

    let mut queue = VecDeque::<(GameState, i32)>::from([(state, 0)]);
    let mut visited = HashMap::<String, i32>::new();
    let mut min_moves = i32::MAX;

    while !queue.is_empty() {
        let (state, num_moves) = queue.pop_front().unwrap();

        // This path has exceeded current known min, no need to continue.
        if num_moves >= min_moves {
            // println!("exceeds min: {}", min_moves);
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
            // println!("new win state: {}", num_moves);
            min_moves = num_moves;
            continue;
        }

        // Finally check state validity and toss it if invalid.
        if !state_is_valid(&state) {
            // println!("state invalid");
            visited.insert(key_for_state(&state), 0);   // Small optimization to not check this again for these states.
            continue;
        }

        let cur_floor = state.floors.get(state.cur_floor).unwrap();

        // We will enqueue some different states to try... first we will remove item from cur floor.
        for item in cur_floor {

            // Queue move up
            if state.cur_floor < num_floors-1 {

                // Now we will try moving pairs...
                let mut can_move_pair = false;
                for item2 in cur_floor.iter() {
                    if item2 == item {
                        continue;
                    }

                    // Any two items can move together unless it's a Chip/Gen combo with different elements
                    let is_safe = match item {
                        Item::Generator(el) => match item2 {
                            Item::Generator(_) => true,
                            Item::Microchip(el2) => el == el2
                        },
                        Item::Microchip(el) => match item2 {
                            Item::Generator(el2) => el == el2,
                            Item::Microchip(_) => true
                        }
                    };

                    if is_safe { 
                        // Queue move up
                        // if state.cur_floor < num_floors-1 {
                            let new_state = move_floors(&state, item, state.cur_floor, state.cur_floor+1).unwrap();
                            let new_state = move_floors(&new_state, item2, state.cur_floor, state.cur_floor+1).unwrap();
                            queue.push_back((new_state, num_moves+1));
                            can_move_pair = true;
                        // }

                        // Queue move down - don't bother moving a pair down.
                        // if state.cur_floor > 0 {
                        //     let new_state = move_floors(&state, item, state.cur_floor, state.cur_floor-1).unwrap();
                        //     let new_state = move_floors(&new_state, item2, state.cur_floor, state.cur_floor-1).unwrap();
                        //     queue.push_back((new_state, num_moves+1));
                        // }
                    }
                }

                // Only move one up if can't move a pair.
                if !can_move_pair {
                    let new_state = move_floors(&state, item, state.cur_floor, state.cur_floor+1).unwrap();
                    queue.push_back((new_state, num_moves+1));
                }
            }

            // Queue move down
            if state.cur_floor > 0 {
                let new_state = move_floors(&state, item, state.cur_floor, state.cur_floor-1).unwrap();
                queue.push_back((new_state, num_moves+1));
            }
        }
    }

    println!("min moves: {}", min_moves);
}