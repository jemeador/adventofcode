use std::env;
use std::fs;
use regex::Regex;

fn get_mul(contents : &str) -> i32 {
    let mul_re = Regex::new(r"mul\([0-9]+,[0-9]+\)").unwrap();
    let caps = mul_re.find_iter(contents);

    let mut total : i32 = 0;

    for cap in caps {
        let m = cap.as_str();
        let len = m.len();
        let num_str = &m[4..len-1];
        let nums : Vec<_>= num_str.split(",").collect();
        if nums.len() == 2 {
            total += nums[1].parse::<i32>().expect("Not a number?") * nums[0].parse::<i32>().expect("Not a number?");
        }
        println!("{}", num_str);
    }
    return total;
}

fn main() {
    let args: Vec<String> = env::args().collect();

    let file_path = &args[1];

    let contents = fs::read_to_string(file_path)
        .expect("Should have been able to read the file");

    println!("Solution 1: {}", get_mul(contents.as_str()));

    // let lines: Vec<String> = contents.lines().map(String::from).collect();

    let mut i = 0;
    let mut solution_2 : i32 = 0;
    let mut enabled : bool = true;
    loop {
        let new_contents : String = contents.chars().skip(i).collect();
        let dont_token = "don't()";
        let dont_index = new_contents.find(dont_token);
        if dont_index.is_none() {
            break;
        }
        let j = dont_index.expect("um");
        solution_2 += get_mul(&contents[i..i+j]);
        enabled = false;
        i += dont_index.expect("um") + dont_token.len();
        let do_contents : String = contents.chars().skip(i).collect();
        let do_token = "do()";
        let do_index = do_contents.find(do_token);
        if do_index.is_none() {
            break;
        }
        i += do_index.expect("um") + do_token.len();
        enabled = true;
    }
    if enabled {
        solution_2 += get_mul(&contents[i..]);
    }

    //let do_iter = contents.find("do()");
    //rintln!("{}", do_iter.expect("OK"));
    //println!("{}", dont_iter.expect("OK"));

    println!("Solution 2: {}", solution_2);
}
