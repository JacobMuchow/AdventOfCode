#![allow(dead_code)]

use md5;

fn md5_hash(str: String) -> String {
    let digest = md5::compute(str);
    return format!("{:x}", digest);
}

pub fn run() {
    // let door_id = String::from("abc");
    let door_id = String::from("wtnhxymk");
    let mut index = -1;

    let mut password = String::from("........");
    let mut filled = 0;

    while filled < 8 {
        index += 1;

        let val = format!("{}{}", door_id, index);
        let hash = md5_hash(val);

        if hash.starts_with("00000") {
            let pos_raw = hash.chars().nth(5).unwrap();
            if pos_raw < '0' || pos_raw > '7' {
                continue;
            }

            let pos: usize = pos_raw.to_string().parse().unwrap();
            let mut chars: Vec<char> = password.chars().collect();

            if chars[pos] != '.' {
                continue;
            }

            let value = hash.chars().nth(6).unwrap();

            chars[pos] = value;
            password = chars.into_iter().collect();
            filled += 1;
        }
    }

    println!("Password: {}", password);
}