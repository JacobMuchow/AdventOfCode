#![allow(dead_code)]

use std::collections::VecDeque;
use crate::shared::md5::md5_hash;

type Pos2d = (usize, usize);

fn dis_to_goal(pos: &Pos2d, goal: &Pos2d) -> usize {
    (goal.1 - pos.1) + (goal.0 - pos.0)
}

// True for direction if door is Open or order UDLR
fn check_directions(key: &String) -> (bool, bool, bool, bool) {
    let hash: Vec<char> = md5_hash(key).chars().collect();

    let door_open = |c: char| -> bool {
        ['b', 'c', 'd', 'e', 'f'].contains(&c)
    };

    return (
        door_open(hash[0]),
        door_open(hash[1]),
        door_open(hash[2]),
        door_open(hash[3])
    )
}

fn priority_enqueue(queue: &mut VecDeque<QueueItem>, item: QueueItem) -> () {
    for i in 0..queue.len() {
        if item.dis <= queue[i].dis {
            queue.insert(i, item);
            return;
        }
    }

    queue.push_back(item);
}

struct QueueItem {
    pos: Pos2d,
    key: String,
    steps: usize,
    dis: usize
}

pub fn run() {
    let passcode = String::from("awrkjxxr");

    let start: Pos2d = (0, 0);
    let goal: Pos2d = (3, 3);
    let grid_w: usize = 4;
    let grid_h: usize = 4;

    // let mut visited: HashSet<String> = HashSet::new();
    let mut min_steps = usize::MAX;
    let mut min_path = String::from("");
    let mut queue = VecDeque::<QueueItem>::from([
        QueueItem { pos: start, key: passcode.clone(), steps: 0, dis: dis_to_goal(&start, &goal) }
    ]);

    while !queue.is_empty() {
        let QueueItem { pos, key, steps, dis: _ } = queue.pop_front().unwrap();

        if steps >= min_steps {
            continue;
        }

        if pos == goal {
            min_steps = steps;
            min_path = key.clone();
            continue;
        }

        let (up, down, left, right) = check_directions(&key);

        if up && pos.1 > 0 {
            let new_pos: Pos2d = (pos.0, pos.1-1);
            priority_enqueue(&mut queue, QueueItem { pos: new_pos, key: key.clone() + "U", steps: steps+1, dis: dis_to_goal(&new_pos, &goal) });
        }

        if down && pos.1 < grid_h-1 {
            let new_pos: Pos2d = (pos.0, pos.1+1);
            priority_enqueue(&mut queue, QueueItem { pos: new_pos, key: key.clone() + "D", steps: steps+1, dis: dis_to_goal(&new_pos, &goal) });
        }

        if left && pos.0 > 0 {
            let new_pos: Pos2d = (pos.0-1, pos.1);
            priority_enqueue(&mut queue, QueueItem { pos: new_pos, key: key.clone() + "L", steps: steps+1, dis: dis_to_goal(&new_pos, &goal) });
        }

        if right && pos.0 < grid_w-1 {
            let new_pos: Pos2d = (pos.0+1, pos.1);
            priority_enqueue(&mut queue, QueueItem { pos: new_pos, key: key.clone() + "R", steps: steps+1, dis: dis_to_goal(&new_pos, &goal) });
        }
    }

    println!("Shortest path found: {}, {}", min_steps, &min_path[passcode.len()..min_path.len()]);
}