use std::fs::File;
use std::io::Read;
use std::path::Path;

fn main() {
    println!("Hello there");

    let path = Path::new("src/input.txt");
    println!("Going to read from file... '{}'", path.display());

    let mut file = match File::open(&path) {
        Err(why) => panic!("Error opening file '{}': {}", path.display(), why),
        Ok(file) => file,
    };

    let mut contents = String::new();
    match file.read_to_string(&mut contents) {
        Err(why) => panic!("Error reading data from file '{}', {}", path.display(), why),
        Ok(_) => ()
    }

    println!("{}", contents);
}
