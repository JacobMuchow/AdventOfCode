#![allow(dead_code)]

use std::collections::VecDeque;
use crate::shared::md5::md5_hash;

type Pos2d = (usize, usize);

struct QueueItem {
    pos: Pos2d,
    key: String,
    steps: usize,
    dis: usize
}

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

fn enqueue(queue: &mut VecDeque<QueueItem>, item: QueueItem) -> () {
    queue.push_back(item);
}

/*
Easy enough to update for pt 2, we simply need to remove the restriction min_steps optimization and exhaust all possible paths.
We can also get rid of priority_enqueue() which is unnecessary since we want to check all paths now.
*/
pub fn run() {
    let passcode = String::from("awrkjxxr");

    let start: Pos2d = (0, 0);
    let goal: Pos2d = (3, 3);
    let grid_w: usize = 4;
    let grid_h: usize = 4;

    let mut max_steps = 0;
    let mut queue = VecDeque::<QueueItem>::from([
        QueueItem { pos: start, key: passcode.clone(), steps: 0, dis: dis_to_goal(&start, &goal) }
    ]);

    while !queue.is_empty() {
        let QueueItem { pos, key, steps, dis: _ } = queue.pop_front().unwrap();

        if pos == goal {
            max_steps = max_steps.max(steps);
            continue;
        }

        let (up, down, left, right) = check_directions(&key);

        if up && pos.1 > 0 {
            let new_pos: Pos2d = (pos.0, pos.1-1);
            enqueue(&mut queue, QueueItem { pos: new_pos, key: key.clone() + "U", steps: steps+1, dis: dis_to_goal(&new_pos, &goal) });
        }

        if down && pos.1 < grid_h-1 {
            let new_pos: Pos2d = (pos.0, pos.1+1);
            enqueue(&mut queue, QueueItem { pos: new_pos, key: key.clone() + "D", steps: steps+1, dis: dis_to_goal(&new_pos, &goal) });
        }

        if left && pos.0 > 0 {
            let new_pos: Pos2d = (pos.0-1, pos.1);
            enqueue(&mut queue, QueueItem { pos: new_pos, key: key.clone() + "L", steps: steps+1, dis: dis_to_goal(&new_pos, &goal) });
        }

        if right && pos.0 < grid_w-1 {
            let new_pos: Pos2d = (pos.0+1, pos.1);
            enqueue(&mut queue, QueueItem { pos: new_pos, key: key.clone() + "R", steps: steps+1, dis: dis_to_goal(&new_pos, &goal) });
        }
    }

    println!("Longest path found: {}", max_steps);
}