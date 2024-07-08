#![allow(dead_code)]

use std::collections::BTreeSet;

use map_macro::btree_set;

/*
    It's immediately obvious a naive solution would take up too much space/time, and the example tries to hide the obvious pattern
    which is that for the most part the difference betwen every "number" of elf left is the same in the middle of the set. It is only
    at the ends that unique things may happen. I figured there is a way we can track the lower bound number(s) and upper and derive
    everything else from there, if we also track # of elves left & what turn we are on, i.e. the "group size" or distance between elves
    in the middle.

    After doing a couple examples by hand with low numbers, I saw a pattern begin to develop... when the collection is even, then no "wrap"
    around occurs, and when it's odd, then the last element "eats" the first one. This is consistent for any size "n", and we can come up
    with some generalized rules for how to compute these edges.

    My first pass I tracked the values indices 0, 1 ... n-1, n. Which did lead me to a correct solution. Though I'm somewhat confident you could
    also make a solution keeping track of only 1 number on each end instead of since the other should be derivable.

    Runs in 29us :)
*/
pub fn run() {
    let num_elves = 3005290;

    let mut group_size = 1;
    let mut elves_left = num_elves;

    let mut lower = [1, 2];
    let mut upper = [num_elves-1, num_elves];

    // This generalization makes sense so long as #left is > 4. 
    // After that we can pick the winner using some different logic.
    while elves_left > 4 {
        let even_total = elves_left % 2 == 0;
        elves_left /= 2;
        group_size *= 2;

        // lower[0] never changes on its own. only when upper[1] overlaps.

        // lower[1] is eaten by lower[0] so we need to compute a new lower[1].
        lower[1] = lower[0] + group_size;

        if even_total {
            // upper[0] eats upper[1].
            upper[1] = upper[0];

            // compute new upper[0].
            upper[0] = upper[1] - group_size;
        } else {
            // upper[0] is eaten by whatever precedes it. We can derive this.
            upper[0] = upper[1] - group_size;

            // Lower zero is eaten by upper[1].
            // Lower[1] becomes the new lower[0].
            lower[0] = lower[1];
            // Compute the new lower[1].
            lower[1] = lower[0] + group_size;
        }
    }

    // There may be overlap/repeats, depending on the original number, so we will make an ordered set from the numbers left.
    let last_elves: BTreeSet<i32> = btree_set! {
        lower[0], lower[1], upper[0], upper[1]
    };

    println!("Lower: {:?}", lower);
    println!("Upper: {:?}", upper);

    // In a system with 2 or 4 remaining, 0 idx will win. This is true for any collection with a len of 2^n in fact.
    // In a system with 3 remaining, n-1 idx will win.
    // Knowing this we can just select the winner as first or last element based on evenness. 
    let winner = if last_elves.len() % 2 == 0 { last_elves.first() } else { last_elves.last() };
    println!("Winner: {}", winner.unwrap());
}