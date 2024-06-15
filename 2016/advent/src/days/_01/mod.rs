use std::fs::read_to_string;

fn read_lines(path: &str) -> Vec<String> {
    read_to_string(path)
        .unwrap()
        .lines()
        .map(String::from)
        .collect()
}

pub fn run(path: &str) {
    let lines = read_lines(path);
    for line in lines {
        println!("{}", line);
    }
}