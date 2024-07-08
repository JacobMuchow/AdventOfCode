#![allow(dead_code)]

fn is_trap(prev_line: &Vec<char>, i: usize) -> bool {
    // true = safe, false = trap
    let l: bool = if i == 0 { true } else { prev_line[i-1] == '.' };
    let c: bool = prev_line[i] == '.';
    let r: bool = if i == prev_line.len()-1 { true } else { prev_line[i+1] == '.' };

    (!l && !c &&  r) ||
    ( l && !c && !r) ||
    (!l &&  c &&  r) ||
    ( l &&  c && !r)
}

pub fn run() {
    let line = ".^^.^.^^^^";
    let num_rows = 10;

    let line = ".^^^.^.^^^.^.......^^.^^^^.^^^^..^^^^^.^.^^^..^^.^.^^..^.^..^^...^.^^.^^^...^^.^.^^^..^^^^.....^....";
    let num_rows = 40;

    let mut grid: Vec<Vec<char>> = vec![
        line.chars().collect()
    ];

    while grid.len() < num_rows {
        let last = grid.last().unwrap();
        let mut new = last.clone();

        for i in 0..new.len() {
            new[i] = if is_trap(last, i) { '^' } else { '.' };
        }

        grid.push(new);
    }

    let mut num_safe = 0;
    for line in grid {
        for c in line {
            if c == '.' {
                num_safe += 1;
            }
        }
    }

    println!("Num safe: {}", num_safe);
}