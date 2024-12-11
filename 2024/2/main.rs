use std::env;
use std::fs;

fn sign(number: i32) -> i32 {
    if number > 0 {
        return 1;
    }
    else if number < 0 {
        return -1;
    }
    return 0;
}

fn main() {
    let args: Vec<String> = env::args().collect();

    let file_path = &args[1];

    let contents = fs::read_to_string(file_path)
        .expect("Should have been able to read the file");

    let lines: Vec<String> = contents.lines().map(String::from).collect();

    let mut solution_1 : i32 = 0;
    let mut solution_2 : i32 = 0;

    for line in lines {
        let numbers : Vec<_> = line.split_whitespace().map(str::parse::<i32>).collect();
        for skip_index in -1..(numbers.len() as i32) {
            let mut safe : bool = true;
            let mut prev_number : i32 = -1;
            let mut prev_delta : i32 = 0;
            for pair in numbers.iter().enumerate() {
                if pair.0 as i32 == skip_index {
                    continue;
                }
                let number = pair.1.clone().expect("Could not read int");
                if prev_number == -1 {
                    prev_number = number;
                    continue;
                }
                let delta = number - prev_number;
                if delta.abs() < 1 || delta.abs() > 3 {
                    safe = false;
                    break;
                }
                if prev_delta != 0 {
                    let this_sign = sign(delta);
                    let prev_sign = sign(prev_delta);
                    if this_sign != prev_sign {
                        safe = false;
                        break;
                    }
                }
                prev_number = number;
                prev_delta = delta;
            }
            if safe && skip_index == -1 {
                solution_1 += 1;
            }
            if safe {
                solution_2 += 1;
                break;
            }
        }
    }

    println!("Solution 1: {}", solution_1);

    println!("Solution 2: {}", solution_2);
}
