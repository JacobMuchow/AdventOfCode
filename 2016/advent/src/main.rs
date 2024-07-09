use std::time::Instant;

// use shared::lists::first::List;

mod days;
mod shared;
// mod shared::lists;

fn run_solution() {
    // days::_19::pt2::run();

    // let list: List = List::Elem(3, Box::new(List::Elem(4, Box::new(List::Empty))));
    // println!("{:?}", list);
}

fn main() {
    println!("Running solution...");
    let start = Instant::now();
    run_solution();
    
    let duration = start.elapsed();
    println!("Solution ran in {:?}", duration);
}
