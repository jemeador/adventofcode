use std::env;
use std::fs;
use intbits::Bits;

fn main() {
    let args: Vec<String> = env::args().collect();
    let file_path = &args[1];
    let contents = fs::read_to_string(file_path)
        .expect("Should have been able to read the file");
    let lines: Vec<String> = contents.lines().map(String::from).collect();
    let mut solution_1 = 0;
    let mut solution_2 = 0;
    for line in lines {
        let line = line.replace(':', "");
        let numbers : Vec<i64> = line.split_whitespace().map(str::parse::<i64>).map(|result| result.expect("Not a page number")).collect();
        //println!("{:?}", numbers);

        let lhs = numbers[0];
        let equation_nums = &numbers[1..];
        let operators_len = equation_nums.len() - 1;
        let part_1_max = 2_i64.pow(operators_len.try_into().unwrap());
        let part_2_max = 3_i64.pow(operators_len.try_into().unwrap());
        //println!("{:?}", part_1_max);

        for i in 0..part_1_max {
            let mut rhs = equation_nums[0];
            for b in 0..operators_len {
                if i.bit(b) {
                    rhs += equation_nums[b + 1];
                }
                else {
                    rhs *= equation_nums[b + 1];
                }
            }
            if lhs == rhs {
                //print!("{} = {}", rhs, equation_nums[0]);
                //for b in 0..operators_len {
                //    if i.bit(b) {
                //        print!(" + ");
                //    }
                //    else {
                //        print!(" * ");
                //    }
                //    print!("{}", equation_nums[b + 1]);
                //}
                //println!();
                solution_1 += lhs;
                break;
            }
        }

        println!("{:?}", part_2_max);

        for i in 0..part_2_max {
            let mut ternary_digits : Vec<i64> = Vec::new();
            ternary_digits.resize(operators_len, 0);
            let mut part_2_val = i;
            let mut n = 0;
            while part_2_val > 0 {
                ternary_digits[n] = (part_2_val % 3);
                part_2_val /= 3;
                n += 1;
            }
            println!("{:?}", ternary_digits);

            let mut rhs = equation_nums[0];
            let mut error_free = true;
            for b in 0..operators_len {
                if ternary_digits[b] == 0 {
                    rhs += equation_nums[b + 1];
                }
                else if ternary_digits[b] == 1 {
                    rhs *= equation_nums[b + 1];
                }
                else {
                    let parse_result = str::parse::<i64>(&(rhs.to_string() + &equation_nums[b+1].to_string()));
                    if parse_result.is_err() {
                        error_free = false;
                        break;
                    }
                    else {
                        rhs = parse_result.expect("We checked for parse error?");
                    }
                }
            }
            if error_free && lhs == rhs {
                print!("{} = {}", rhs, equation_nums[0]);
                for b in 0..operators_len {
                    if ternary_digits[b] == 0 {
                        print!(" + ");
                    }
                    else if ternary_digits[b] == 1 {
                        print!(" * ");
                    }
                    else {
                        print!(" || ");
                    }
                    print!("{}", equation_nums[b + 1]);
                }
                println!();
                solution_2 += lhs;
                break;
            }
        }
    }

    // Print the Vec<Vec<char>>
    println!("Solution 1: {}", solution_1);

    println!("Solution 2: {}", solution_2);
}
