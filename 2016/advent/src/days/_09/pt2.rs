#![allow(dead_code)]

use regex::Regex;

use crate::shared::io::read_lines_from_file;

fn decompress(input: &String) -> String {
    let mut output = String::from("");

    let marker_re = Regex::new(r"^\(([0-9]+)x([0-9]+)\)").unwrap();

    let chars: Vec<char> = input.chars().collect();
    let mut i = 0;
    while i < chars.len() {
        if chars[i] != '(' {
            output.push(chars[i]);
            i += 1;
            continue;
        }

        let slice = &input[i..];
        let Some(caps) = marker_re.captures(slice) else {
            output.push(chars[i]);
            i += 1;
            continue;
        };

        let char_count: usize = caps.get(1).unwrap().as_str().parse().unwrap();
        let repeat_count: usize = caps.get(2).unwrap().as_str().parse().unwrap();
        let start_index: usize = caps.get(2).unwrap().end()+1;
        let end_index: usize = start_index + char_count;

        // Pretty easy change. Because of the way we wrote our function,
        // all we need to do is recursively decompress the segments we
        // are going to repeat.
        let repeat_slice = String::from(&slice[start_index..end_index]);
        let repeat_slice_decompressed = decompress(&repeat_slice);

        for _ in 0..repeat_count {
            output.push_str(&repeat_slice_decompressed);
        }
        i += end_index;
    }

    return output;
}

pub fn run() {
    let lines = read_lines_from_file("src/days/_09/input.txt");
    let input = &lines[0];

    /*
    (3x3)XYZ still becomes XYZXYZXYZ, as the decompressed section contains no markers.
    X(8x2)(3x3)ABCY becomes XABCABCABCABCABCABCY, because the decompressed data from the (8x2) marker is then further decompressed, thus triggering the (3x3) marker twice for a total of six ABC sequences.
    (27x12)(20x12)(13x14)(7x10)(1x12)A decompresses into a string of A repeated 241920 times.
    (25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN becomes 445 characters long.
     */

    let output = decompress(&input);

    // The output it too long to print quickly.
    // Technically you could make this all more efficient by just _counting_
    // the characters that would have appeared in the decompressed output, but
    // writing the decompressing algo is a little more fun to me.
    // println!("{}  -->  {}", input, output);

    println!("Decompress length: {}", output.len());
}