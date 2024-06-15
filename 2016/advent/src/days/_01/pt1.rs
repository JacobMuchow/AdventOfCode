use std::fs::read_to_string;
use regex::Regex;

fn read_lines(path: &str) -> Vec<String> {
    read_to_string(path)
        .unwrap()
        .lines()
        .map(String::from)
        .collect()
}

pub fn run() {
    let lines = read_lines("src/days/_01/input.txt");
    let line = lines.get(0).unwrap();

    println!("{}", line);

    let re = Regex::new(r"([LR])([0-9]+)").unwrap();

    let directions = re.captures_iter(line.as_str()).map(|caps| {
        let dir = caps.get(1).map(|m| m.as_str()).unwrap();
        let dist = caps.get(2).map(|m| m.as_str()).unwrap();

        (dir, dist)
    });

    for dir in directions {
        println!("{}{}", dir.0, dir.1);
    }
}