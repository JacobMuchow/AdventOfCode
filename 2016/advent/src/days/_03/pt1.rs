use crate::shared::io::read_lines_from_file;
use regex::Regex;

pub fn run() {
    let lines = read_lines_from_file("src/days/_03/input.txt");

    let mut potential_triangles: Vec<(u32, u32, u32)> = Vec::new();
    let re = Regex::new(r"([0-9]+)\s+([0-9]+)\s+([0-9]+)").unwrap();

    for line in lines {
        let caps = re.captures(&line).unwrap();

        potential_triangles.push((
            caps[1].parse().unwrap(),
            caps[2].parse().unwrap(),
            caps[3].parse().unwrap(),
        ))
    }

    let mut num_possible = 0_u32;

    for sides in potential_triangles {
        let (s1, s2, s3) = sides;
        let max = s1.max(s2).max(s3);

        if s1+s2 > max && s1+s3 > max && s2+s3 > max {
            num_possible += 1;
        }
    }

    println!("Num possible: {}", num_possible);
}