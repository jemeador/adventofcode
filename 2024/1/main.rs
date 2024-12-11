use std::env;
use std::fs;

fn main() {
    let args: Vec<String> = env::args().collect();

    let file_path = &args[1];

    let contents = fs::read_to_string(file_path)
        .expect("Should have been able to read the file");

    let lines: Vec<String> = contents.lines().map(String::from).collect();

    let mut list1 = Vec::new();
    let mut list2 = Vec::new();

    for line in lines {
        for pair in line.split_whitespace().map(str::parse::<i32>).enumerate() {
            let number = pair.1.expect("Could not read int");
            if pair.0 == 0 {
                list1.push(number);
            }
            if pair.0 == 1 {
                list2.push(number);
            }
        }
    }

    list1.sort();
    list2.sort();

    let mut total : i32 = 0;

    for n in 0..list1.len() {
        total += (list1[n] - list2[n]).abs();
    }

    println!("Solution 1: {}", total);

    let mut sim_score : i32 = 0;

    for left in list1 {
        for right in &list2 {
            if left == *right {
                sim_score += left;
            }
        }
    }

    println!("Solution 2: {}", sim_score);
}
