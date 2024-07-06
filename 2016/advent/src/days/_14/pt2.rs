#![allow(dead_code)]

use md5;

fn md5_hash(str: &String) -> String {
    let digest = md5::compute(str);
    format!("{:x}", digest)
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

fn stretch_hash(str: &String) -> String {
    let mut hash = md5_hash(str);
    for _ in 0..2016 {
        hash = md5_hash(&hash);
    }
    hash
}

pub fn run() {
    // let salt = String::from("abc");
    let salt = String::from("cuanljph");
    let mut idx: usize = 0;
    let mut candidate_keys: Vec<Candidate> = Vec::new();
    let mut valid_keys: Vec<Candidate> = Vec::new();

    /*
        To prevent an O(mn) solution, I am going to use one loop to both add "candidates" to a list, 
        and check for candidate matches. Technically this is till O(an) I guess, but a will only be 
        a handful, whereas m can be up to 1000. Runs in 735ms. Having tested the more naive O(mn) 
        solution this is in fact much faster.
     */
    while valid_keys.len() < 64 || !candidate_keys.is_empty() {
        // Pretty easy change, just need to call another hashing function here that will hash 2017 times in a loop.
        // First pass on this runs in 110s debug / 35s release... wonder if any hashes repeat?
        let hash_key = stretch_hash(&format!("{}{}", salt, idx));

        if idx % 1000 == 0 {
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
        // 
        // We want to contineu looping even after 64 valid keys are found, because
        // it is possible a candidate with an earlier index than the current "64th"
        // will still be found to be valid. We sort the list upon exiting by index
        // because it then may end up with more than 64.
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