#![allow(dead_code)]

use index_list::{IndexList, ListIndex};

fn advance<T>(circle: &IndexList<T>, index: ListIndex) -> ListIndex {
    let next = circle.next_index(index);
    let res = if next.is_none() {
        circle.first_index()
    } else {
        next
    };

    // println!("Advance to {}", res);
    res
}

fn remove_elf<T>(circle: &mut IndexList<T>, index: ListIndex) -> ListIndex {
    // println!("Remove {}", index);
    let next = advance(circle, index);
    circle.remove(index);
    next
}

fn index_across<T>(circle: &IndexList<T>, index: ListIndex) -> ListIndex {
    let mut dist = circle.len() / 2;
    let mut cur_index = index;

    while dist > 0 {
        cur_index = circle.next_index(cur_index);
        if cur_index.is_none() {
            cur_index = circle.first_index();
        }
        dist -= 1;
    }
    cur_index
}

/*
    ugh... my solution feels heavily tailored to the first problem after the curve ball, though I don't feel bad about it since 
    it ran in 25 us. I will need to go back to the drawing board and do some small solutions by hand again. 
    Hopefully I can construct a similar generalization...

    After some playing, I found a repeatable pattern where 2 elves are deleted, next is skipped, 2 deleted, 1 skipped, ad infinitum.
    Down to some small circle size like 5 or so because this doesn't work on the example problem.

    Processing my list this way, I made a solution than ran in a hilarious ~600 seconds (10 minutes!!). Since I am not doing anything
    crazy logically, my gut instinct told me this is due to time complexity of remove on Vectors (O(n) iirc). The proper data type
    I can think of for this problem would be a Doubly LinkedList which would give us remove O(1). Furthermore we don't really need
    to do index math with our pattern, just have a cursor so that plays nicely. Little did I know that Rust and Doubly LinkedList are not
    exactly friends... I spend several days in a rabbit whole learning about Rust memory management, and after my endeavor settled for
    a handy, and somewhat popular, IndexList library, which should suit my performance needs. After updating my algorithm now runs in...
    1.7s in Debug, 138ms in Release. Nice.
*/
pub fn run() {
    let num_elves = 3005290;
    // let num_elves = 20;

    let mut circle: IndexList<usize> = IndexList::new();
    for i in 1..=num_elves {
        circle.insert_last(i);
    }

    let start_i = (circle.len() / 2) as i32;
    let mut cur_index = circle.move_index(circle.first_index(), start_i);

    while circle.len() > 10 {
        // if circle.len() % 10000 == 0 {
        //     println!("Circle: {}", circle.len());
        // }

        cur_index = remove_elf(&mut circle, cur_index);
        cur_index = remove_elf(&mut circle, cur_index);
        cur_index = advance(&circle, cur_index);
    }

    // At the moment, cur_index represents the next elf to be deleted following the pattern.
    // We can derive backwards to which elf's "turn" it is, then proceed with a more naive 
    // approach -- the pattern doesn't hold up under some N number of elves, possibly 5.
    cur_index = index_across(&circle, cur_index);

    // Now we will proceed with a conventional turn-by-turn
    // loop.
    while circle.len() > 1 {
        let del_index = index_across(&circle, cur_index);
        circle.remove(del_index);

        cur_index = advance(&circle, cur_index);
    }

    println!("Last elf: {}", circle.first_index());
}