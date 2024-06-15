use crate::shared::io::read_lines_from_file;

pub fn run() {
    let lines = read_lines_from_file("src/days/_03/test.txt");
    for line in lines {
        println!("{}", line);
    }
}