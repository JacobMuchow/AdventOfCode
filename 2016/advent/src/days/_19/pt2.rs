#![allow(dead_code)]

/*
    ugh... my solution feels heavily tailored to the first problem after the curve ball, though I don't feel back about it since 
    it ran in 25 us. I will need to go back to the drawing board and do some small solutions by hand again. 
    Hopefully I can construct a similar generalization. 

    Actually... I'm finding this a little confusing to consider though I'm sure there is a generalizable pattern.
    I'm just going to be lazy and try a naive solution. 3005290 * i32 ~= 12 MB, and the iter count
    will half for each iteration so the compute may not be too bad either.
*/
pub fn run() {
    // let num_elves = 3005290;
    let num_elves = 5;

    let mut circle: Vec<usize> = Vec::new();
    for i in 1..=num_elves {
        circle.push(i);
    }

    let mut del_i = circle.len() / 2;


    while circle.len() > 2 {
        if circle.len() % 10000 == 0 {
            println!("Circle: {}", circle.len());
        }
        circle.remove(del_i);

        if del_i == circle.len() {
            del_i = 0;
        }

        circle.remove(del_i);

        if del_i == circle.len() {
            del_i = 0;
        }

        del_i += 1;

        if del_i == circle.len() {
            del_i = 0;
        }
    }

    println!("Remaining elves: {:?}", circle);

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