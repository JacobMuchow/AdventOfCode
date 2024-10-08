use std::time::Instant;

mod days;
mod shared;

fn run_solution() {
    days::_25::pt1::run();
}

fn main() {
    println!("Running solution...");
    let start = Instant::now();
    run_solution();

    let duration = start.elapsed();
    println!("Solution ran in {:?}", duration);
}
