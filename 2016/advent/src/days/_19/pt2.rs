#![allow(dead_code)]

use index_list::{IndexList, ListIndex};

fn advance<T>(list: &IndexList<T>, index: ListIndex) -> ListIndex {
    let next = list.next_index(index);
    let res = if next.is_none() {
        list.first_index()
    } else {
        next
    };

    // println!("Advance to {}", res);
    res
}

fn remove_elf<T>(list: &mut IndexList<T>, index: ListIndex) -> ListIndex {
    // println!("Remove {}", index);
    let next = advance(list, index);
    list.remove(index);
    next
}

// use crate::shared::doubly_linked_list::LinkedList;

/*
    ugh... my solution feels heavily tailored to the first problem after the curve ball, though I don't feel back about it since 
    it ran in 25 us. I will need to go back to the drawing board and do some small solutions by hand again. 
    Hopefully I can construct a similar generalization. 

    Actually... I'm finding this a little confusing to consider though I'm sure there is a generalizable pattern.
    I'm just going to be lazy and try a naive solution. 3005290 * i32 ~= 12 MB, and the iter count
    will half for each iteration so the compute may not be too bad either.
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
        if circle.len() % 10000 == 0 {
            println!("Circle: {}", circle.len());
        }

        cur_index = remove_elf(&mut circle, cur_index);
        cur_index = remove_elf(&mut circle, cur_index);
        cur_index = advance(&circle, cur_index);
    }

    println!("Remaining elves:");
    for item in circle.iter() {
        println!("{}", item);
    }

    // let mut turn_i = 0;

    // while circle.len() > 1 {
    //     if circle.len() % 10000 == 0 {
    //         println!("Num left: {}", circle.len());
    //     }
    //     let opposite_j = (turn_i + circle.len()/2) % circle.len();
    //     circle.remove(opposite_j);

    //     turn_i = (turn_i+1) % circle.len();
    // }

    // println!("Last elf: {}", circle[0]);
}