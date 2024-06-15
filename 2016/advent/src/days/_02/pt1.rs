use crate::shared::io::read_lines_from_file;

pub fn run() {

    let lines = read_lines_from_file("src/days/_02/test.txt");
    let line = lines.get(0).unwrap();

    println!("Money moves: {}", line);
}