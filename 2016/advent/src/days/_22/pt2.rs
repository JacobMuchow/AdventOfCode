#![allow(dead_code)]

use core::num;
use std::collections::{HashMap, VecDeque};

use regex::Regex;

use crate::shared::{io::read_lines_from_file, regex_extensions::ExtensionsTrait};

#[derive(Debug, Clone, Copy)]
enum Type {
    Empty,
    Wall,
    Data,
}

#[derive(Debug, Clone, Copy)]
struct Node {
    pos: Pos2d,
    size: usize,
    used: usize,
    avail: usize,
    pct_used: usize,
    type_: Type,
}

type Pos2d = (usize, usize);
type NodeMap = HashMap<Pos2d, Node>;

#[derive(Debug)]
struct QueueItem {
    node_map: NodeMap,
    data_pos: Pos2d,
    empty_pos: Pos2d,
    goal_dis: usize,
    empty_dis: usize,
    num_steps: usize,
    prev_empty_pos: Pos2d,
}

fn parse_input(file: &str) -> (NodeMap, usize, usize) {
    let mut node_map = NodeMap::new();
    let mut width: usize = 0;
    let mut height: usize = 0;

    let lines = read_lines_from_file(file);
    let re = Regex::new(
        r"^/dev/grid/node-x([0-9]+)-y([0-9]+)\s+([0-9]+)T\s+([0-9]+)T\s+([0-9]+)T\s+([0-9]+)%$",
    )
    .unwrap();

    for i in 2..lines.len() {
        let line = &lines[i];

        let Some(caps) = re.captures(line) else {
            panic!("Failed match from input: {}", line);
        };

        let x: usize = caps.get_as_num(1).unwrap();
        let y: usize = caps.get_as_num(2).unwrap();
        let size: usize = caps.get_as_num(3).unwrap();
        let used: usize = caps.get_as_num(4).unwrap();
        let avail: usize = caps.get_as_num(5).unwrap();
        let pct_used: usize = caps.get_as_num(6).unwrap();
        let pos: Pos2d = (x, y);

        width = width.max(x + 1);
        height = height.max(y + 1);

        node_map.insert(
            pos,
            Node {
                pos,
                size,
                used,
                avail,
                pct_used,
                type_: Type::Data,
            },
        );
    }

    (node_map, width, height)
}

fn determine_types(node_map: &mut NodeMap) {
    for node in node_map.values_mut() {
        if node.used == 0 {
            node.type_ = Type::Empty;
        }
    }
}

fn adjacent_viable_nodes<'a>(
    node_map: &'a NodeMap,
    width: usize,
    height: usize,
    to: &'a Node,
) -> Vec<&'a Node> {
    let mut nodes = Vec::<&Node>::new();
    let (x, y) = to.pos;

    // Left
    if x > 0 {
        let from = node_map.get(&(x - 1, y)).unwrap();
        if can_move(from, to) {
            nodes.push(from);
        }
    }

    // Right
    if x < width - 1 {
        let from = node_map.get(&(x + 1, y)).unwrap();
        if can_move(from, to) {
            nodes.push(from);
        }
    }

    // Up
    if y > 0 {
        let from = node_map.get(&(x, y - 1)).unwrap();
        if can_move(from, to) {
            nodes.push(from);
        }
    }

    // Down
    if y < height - 1 {
        let from = node_map.get(&(x, y + 1)).unwrap();
        if can_move(from, to) {
            nodes.push(from);
        }
    }

    nodes
}

fn priority_enqueue(queue: &mut VecDeque<QueueItem>, item: QueueItem) {
    for i in 0..queue.len() {
        let cmp_item = queue.get(i).unwrap();

        if item.goal_dis > cmp_item.goal_dis || item.empty_dis > cmp_item.empty_dis {
            continue;
        }

        queue.insert(i, item);
        return;
    }
    queue.push_back(item);
}

fn dis(from: Pos2d, to: Pos2d) -> usize {
    from.0.abs_diff(to.0) + from.1.abs_diff(to.1)
}

fn key((x, y): &Pos2d) -> String {
    format!("{},{}", x, y)
}

fn state_hash(node_map: &NodeMap, width: usize, height: usize, data_pos: Pos2d) -> String {
    let mut hash = String::from("");
    hash += &key(&data_pos);
    hash += "|";

    for y in 0..height {
        for x in 0..width {
            let node = node_map.get(&(x, y)).unwrap();
            hash += &format!("{}|", node.used);
        }
    }
    hash
}

fn state_hash_2(data_pos: &Pos2d, empty_pos: &Pos2d) -> String {
    let mut hash = String::from("");
    hash += &key(&data_pos);
    hash += "|";
    hash += &key(&empty_pos);
    return hash;
}

fn can_move(from: &Node, to: &Node) -> bool {
    // if from.pos == to.pos { return false }
    from.used > 0 && from.used <= to.avail
}

fn move_data(node_map: &mut NodeMap, from: &Node, to: &Node) {
    let mut from = from.clone();
    let mut to = to.clone();

    to.used += from.used;
    to.avail = to.size - to.used;
    from.used = 0;
    from.avail = from.size;

    node_map.insert(from.pos, from);
    node_map.insert(to.pos, to);
}

fn print_state(item: &QueueItem, width: usize, height: usize, goal_pos: Pos2d) {
    for y in 0..height {
        for x in 0..width {
            let pos = (x, y);
            if pos == goal_pos {
                print!("G");
            } else if pos == item.data_pos {
                print!("D");
            } else if pos == item.empty_pos {
                print!("_");
            } else {
                let node = item.node_map.get(&(x, y)).unwrap();
                print!("{}", if node.used == 0 { '_' } else { '.' });
            }
        }
        println!()
    }
}

/*
    Part 1 is sort of pointless for the final problem, but if you do a little extra looking,
    you will find that all the "viable" nodes are simply moving to the single empty node. And that
    the only possible moves at the start are to move the adjacent nodes to the empty one (4 total).

    In other words, there is no situation where we may move data from Node A to Node B,
    where Node B has some data used already. Which makes this problem simpler, much like the
    example. It is like a tile-sliding game where you have 1 empty space and need to make a picture.
    But only the 1st step of that where we need to get a specific tile to 0,0. ...And with some extra
    constraints like there may be tiles that can't move at all because they are too large,
    or can't move to certain neighbors that are too small.

    I think we may treat this like a BFS problem with some optimizations to prioritize dequeing:
    - 1) Distance (W)anted node data from (G)oal.
    - 2) Distance (E)mpty node from W.
    - We will also want to create a HashMap of previously visited states and then steps to get there.
        A proper hash could be an ordered list of node used sizes with a delimeter.
    - The goal will be to find a short-ish path to the Goal as soon as possible, then exhaust all other options
        that dead-end or exceed the current goal step count.
*/
pub fn run() {
    let (node_map, width, height) = parse_input("src/days/_22/input.txt");

    // Initialize queue with starting item.
    let goal_pos: Pos2d = (0, 0);
    let data_pos: Pos2d = (width - 1, 0);
    let empty_pos: Pos2d = node_map.values().find(|n| n.used == 0).unwrap().pos;
    let goal_dis = dis(data_pos, goal_pos);
    let empty_dis = dis(empty_pos, data_pos);

    let mut visited = HashMap::<String, usize>::new();
    let mut queue = VecDeque::<QueueItem>::new();
    queue.push_back(QueueItem {
        node_map,
        data_pos,
        empty_pos,
        goal_dis,
        empty_dis,
        num_steps: 0,
        prev_empty_pos: (0, 0),
    });

    let mut min_steps = usize::MAX;
    let mut i = 0;

    while !queue.is_empty() {
        let item = queue.pop_front().unwrap();

        // println!("Iter {}: {:?}", i, empty_pos);
        // print_state(&item, width, height, goal_pos);
        // break;

        if i % 10000 == 0 {
            println!("Iter {}", i);
            // print_state(&item, width, height, goal_pos);
            // println!("\n");
        }
        i += 1;

        let QueueItem {
            node_map,
            data_pos,
            empty_pos,
            goal_dis: _,
            empty_dis: _,
            num_steps,
            prev_empty_pos,
        } = item;

        // Over best step count, ignore.
        if num_steps >= min_steps {
            continue;
        }

        // Reached goal
        if data_pos == goal_pos {
            min_steps = min_steps.min(num_steps);
            println!("Goal found! New min: {}", min_steps);
            continue;
        }

        // Visited this pos in less steps previously, ignore.
        let hash = state_hash_2(&data_pos, &empty_pos);
        if let Some(steps) = visited.get(&hash) {
            // println!("state visited!!! {} vs. cur {}", steps, num_steps);
            if &num_steps >= steps {
                // println!("exit");
                continue;
            }
        }
        visited.insert(hash, num_steps);

        let data_node = node_map.get(&data_pos).unwrap();
        let empty_node = node_map.get(&empty_pos).unwrap();

        // Check viables moves to empty node & enqueue new states..
        let adjacent = adjacent_viable_nodes(&node_map, width, height, empty_node);
        for adj in adjacent {
            if adj.pos == prev_empty_pos {
                continue;
            }

            if can_move(adj, empty_node) {
                // println!("Can move: {:?}", adj.pos);
                let mut node_map = node_map.clone();
                move_data(&mut node_map, adj, &empty_node);

                let prev_empty_pos = empty_pos;
                let empty_pos = adj.pos;
                let data_pos = if adj.pos == data_node.pos {
                    empty_node.pos
                } else {
                    data_node.pos
                };
                let goal_dis = dis(data_pos, goal_pos);
                let empty_dis = dis(empty_pos, data_node.pos);
                let num_steps = num_steps + 1;

                let item = QueueItem {
                    node_map,
                    data_pos,
                    empty_pos,
                    goal_dis,
                    empty_dis,
                    num_steps,
                    prev_empty_pos,
                };
                priority_enqueue(&mut queue, item);
            }
        }
    }

    println!("Min steps found: {}", min_steps);
}
