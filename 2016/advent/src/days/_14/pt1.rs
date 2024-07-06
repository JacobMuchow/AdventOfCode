#![allow(dead_code)]

use md5;

fn md5_hash(str: &String) -> String {
    let digest = md5::compute(str);
    return format!("{:x}", digest);
}

#[derive(Debug, Clone)]
struct Candidate {
    idx: usize,
    key: String,
    search: String
}

fn find_triple(hash: &String) -> Option<char> {
    let chars: Vec<char> = hash.chars().collect();

    for i in 0..chars.len()-2 {
        if chars[i] == chars[i+1] && chars[i] == chars[i+2] {
            return Some(chars[i])
        }
    }
    return None
}

pub fn run() {
    // let salt = String::from("abc");
    let salt = String::from("cuanljph");
    let mut idx: usize = 0;
    let mut candidate_keys: Vec<Candidate> = Vec::new();
    let mut valid_keys: Vec<Candidate> = Vec::new();

    /*
        To prevent an O(mn) solution, I am going to use one loop
        to both add "candidates" to a list, and check for candidate
        matches. Technically this is till O(an) I guess, but a will
        only be a handful, whereas m can be up to 1000. Runs in 735ms.
     */
    while valid_keys.len() < 64 || !candidate_keys.is_empty() {
        let hash_key = md5_hash(&format!("{}{}", salt, idx));

        if idx % 10000 == 0 {
            println!("loop {}", idx);
        }

        // Check canadidates
        let mut i: usize = 0;
        loop {
            if i >= candidate_keys.len() {
                break;
            }

            let candidate = &candidate_keys[i];

            if idx > candidate.idx + 1000 {
                candidate_keys.remove(i);
            }

            else if hash_key.contains(&candidate.search) {
                valid_keys.push(candidate.clone());
                candidate_keys.remove(i);
            }

            else {
                i += 1;
            }
        }

        // Add to candidates (but only if we haven't hit 64 valid yet yet).
        if valid_keys.len() < 64 {
            if let Some(c) = find_triple(&hash_key) {
                let search = format!("{}{}{}{}{}", c, c, c, c, c);
                candidate_keys.push(Candidate { idx, key: hash_key, search });
            }
        }

        idx += 1;
    }

    valid_keys.sort_by_key(|k| k.idx);

    println!("64th key: {:?}", valid_keys[63])
}