use crate::shared::io::read_lines_from_file;

pub fn run() {
    let lines = read_lines_from_file("src/days/_02/input.txt");

    let keypad = [
        [".", ".", "1", ".", "."],
        [".", "2", "3", "4", "."],
        ["5", "6", "7", "8", "9"],
        [".", "A", "B", "C", "."],
        [".", ".", "D", ".", "."],
    ];

    let mut x = 0_i32;
    let mut y = 2_i32;
    let mut keycode = String::from("");

    for line in lines {
        for char in line.chars() {
            let mut new_x = x;
            let mut new_y = y;

            match char {
                'R' => new_x = (x+1).min(4),
                'L' => new_x = (x-1).max(0),
                'U' => new_y = (y-1).max(0),
                'D' => new_y = (y+1).min(4),
                c @ _ => panic!("Unknown char in input: '{}'", c)
            };

            if keypad[new_y as usize][new_x as usize] != "." {
                x = new_x;
                y = new_y;
            }
        }

        keycode.push_str(&keypad[y as usize][x as usize]);
    }

    println!("Keycode: {}", keycode);

}