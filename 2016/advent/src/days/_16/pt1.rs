#![allow(dead_code)]

use std::iter;

fn dragon(disk: &mut Vec<char>, len: usize, max_len: usize) -> usize {
    println!("Dragong called, len: {}, max: {}", len, max_len);
    print_disk(&disk);

    
    if len >= max_len { return len }

    // Add '0' seaparator.
    disk[len] = '0';
    if len+1 >= max_len { return len+1 }

    let new_len = (2*len+1).min(max_len);

    let mut i = len+1;
    let mut j = len-1;
    while i < new_len {
        disk[i] = if disk[j] == '1' { '0' } else { '1' };
        i += 1;
        if j > 0 {
            j -= 1;
        }
    }

    return new_len
}

fn checksum(str: &Vec<char>) -> String {
    let _check_iter = |str: &Vec<char>| {
        let mut chars: Vec<char> = Vec::with_capacity(str.len()/2);

        for i in (0..str.len()).step_by(2) {
            chars.push(if str[i] == str[i+1] { '1' } else { '0' });
        }

        chars
    };

    let mut checksum = _check_iter(str);
    
    while checksum.len() % 2 == 0 {
        checksum = _check_iter(&checksum);
    }

    checksum.iter().collect()
}

fn print_disk(disk: &Vec<char>) -> () {
    let s: String = disk.iter().collect();
    println!("Disk: {}", s);
}

pub fn run() {
    let str: String = iter::repeat('0').take(6).collect();

    let base = String::from("110010110100");
    // let disk_size: usize = 20;

    // let empty_space: String = iter::repeat(' ').take(disk_size - base.len()).collect();
    // let mut disk: Vec<char> = (base.clone() + &empty_space).chars().collect();
    // let mut len = base.len();


    // len = dragon(&mut disk, len, disk_size);
    // print_disk(&disk);

    let checksum = checksum(&base.chars().collect());
    println!("checksum: {}", checksum);
}