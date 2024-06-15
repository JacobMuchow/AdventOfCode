use std::fs::read_to_string;

fn read_lines(path: &str) -> Vec<String> {
    read_to_string(path)
        .unwrap()
        .lines()
        .map(String::from)
        .collect()
}

pub fn run() {
    let lines = read_lines("src/days/_01/input.txt");
    for line in lines {
        println!("{}", line);
    }
}