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

        println!("Range: {} - {}", start_index, end_index);
        let repeat_slice = &slice[start_index..end_index];

        println!("Repeat slice: {}", repeat_slice);
        println!("{}", output);
        for _ in 0..repeat_count {
            output.push_str(repeat_slice);
        }
        i += end_index;
    }

    return output;
}

pub fn run() {
    let lines = read_lines_from_file("src/days/_09/input.txt");
    let input = &lines[0];

    /*
     * 
    ADVENT contains no markers and decompresses to itself with no changes, resulting in a decompressed length of 6.
    A(1x5)BC repeats only the B a total of 5 times, becoming ABBBBBC for a decompressed length of 7.
    (3x3)XYZ becomes XYZXYZXYZ for a decompressed length of 9.
    A(2x2)BCD(2x2)EFG doubles the BC and EF, becoming ABCBCDEFEFG for a decompressed length of 11.
    (6x1)(1x3)A simply becomes (1x3)A - the (1x3) looks like a marker, but because it's within a data section of another marker, it is not treated any differently from the A that comes after it. It has a decompressed length of 6.
    X(8x2)(3x3)ABCY becomes X(3x3)ABC(3x3)ABCY (for a decompressed length of 18), because the decompressed data from the (8x2) marker (the (3x3)ABC) is skipped and not processed further.
     */

    let output = decompress(&input);
    println!("{}  -->  {}", input, output);

    println!("Decompress length: {}", output.len());
}