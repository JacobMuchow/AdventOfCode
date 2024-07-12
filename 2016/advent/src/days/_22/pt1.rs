#![allow(dead_code)]

use std::collections::HashMap;

use regex::Regex;

use crate::shared::{io::read_lines_from_file, regex_extensions::ExtensionsTrait};

#[derive(Debug)]
struct Node {
    pos: Pos2d,
    size: usize,
    used: usize,
    avail: usize,
    pct_used: usize
}

type Pos2d = (usize, usize);

pub fn run() {
    let lines = read_lines_from_file("src/days/_22/input.txt");

    let mut node_map = HashMap::<Pos2d, Node>::new();
    let re = Regex::new(r"^/dev/grid/node-x([0-9]+)-y([0-9]+)\s+([0-9]+)T\s+([0-9]+)T\s+([0-9]+)T\s+([0-9]+)%$").unwrap();

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

        node_map.insert(pos, Node { pos, size, used, avail, pct_used });
    }

    let mut num_viable = 0;

    for node_a in node_map.values() {
        for node_b in node_map.values() {
            // Ignore same node.
            if node_a.pos == node_b.pos {
                continue;
            }

            // Ignore empty A.
            if node_a.used > 0 && node_a.used <= node_b.avail {
                num_viable += 1;
            }
        }
    }

    println!("Num viable nodes: {}", num_viable);
}