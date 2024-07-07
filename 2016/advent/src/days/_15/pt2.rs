#![allow(dead_code)]

#[derive(Clone, Debug)]
struct Disc {
    num: usize,
    total_positions: usize,
    start_position: usize
}

fn calc_pos(disc: &Disc, t: usize) -> usize {
    (t + disc.num + disc.start_position) % disc.total_positions
}

pub fn run() {
    // let discs: Vec<Disc> = vec![
    //     Disc { num: 1, total_positions: 5, start_position: 4 },
    //     Disc { num: 2, total_positions: 2, start_position: 1 }
    // ];

    let discs: Vec<Disc> = vec![
        Disc { num: 1, total_positions: 5, start_position: 2 },
        Disc { num: 2, total_positions: 13, start_position: 7 },
        Disc { num: 3, total_positions: 17, start_position: 10 },
        Disc { num: 4, total_positions: 3, start_position: 2 },
        Disc { num: 5, total_positions: 19, start_position: 9 },
        Disc { num: 6, total_positions: 7, start_position: 0 },
        // Only need to add this. This increases the run time by an order of magnitude
        // (0.5ms -> 5.2ms), but is still quite reasonable.
        Disc { num: 7, total_positions: 11, start_position: 0 }
    ];

    /*
        Each Disc can be considered as an equation of the form: pos = (t + sart + num) % total.
        It's also worth taking note that each modulo is a prime number. There is a math theory
        called Chinese Remainder Theorem we could utilize in this situation. BUT, given
        the relatively small numbers & data set, I think we can reasonly brute force it by finding
        the the first "t" where the largest disc will be at 0, then testing all discs iterating
        "t" by the largest modulo. Eventually the stars will align so to speak.
     */

    // Find first time t where pos is "0" for the largest disc, this should just be a few ticks.
    let largest = discs.iter().max_by_key(|d| d.total_positions).unwrap();

    let mut t = largest.total_positions - largest.start_position - largest.num;

    // Iterate increasing by size of largest disc, until all discs align to 0.
    'outer: loop {
        // In theory I think this might be optimized by first sorting the disks largest to smallest,
        // but in practice this had no effect with this data set so I removed the sort.
        for disc in &discs {
            if calc_pos(&disc, t) != 0 {
                t += largest.total_positions;
                continue 'outer;
            }
        }

        break;
    }

    println!("Good t found: {}", t);
}