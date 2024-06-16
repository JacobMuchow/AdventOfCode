#![allow(dead_code)]

use md5;

fn md5_hash(str: String) -> String {
    let digest = md5::compute(str);
    return format!("{:x}", digest);
}

pub fn run() {
    // let door_id = String::from("abc");
    let door_id = String::from("wtnhxymk");
    let mut index = 0_u32;

    let mut password = String::from("");

    while password.len() < 8 {
        let val = format!("{}{}", door_id, index);
        let hash = md5_hash(val);

        if hash.starts_with("00000") {
            password.push(hash.chars().nth(5).unwrap());
        }

        index += 1;
    }

    println!("Password: {}", password);
}