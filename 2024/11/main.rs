use std::env;
use std::io;
use std::collections::HashMap;
use std::fs;

//#[derive(Debug)]
//#[derive(Clone)]
//struct Span {
//    id : i64,
//    size : u32,
//}

fn blink(memo: & mut HashMap<(u64, u64), u64>, stone : u64, times : u64) -> u64 {
    if times == 0 {
        return 1;
    }
    if let Some(&cache_hit) = memo.get(&(stone, times)) {
        println!("{} {}", stone, times);
        return cache_hit;
    }
    let mut result : u64;
    if stone == 0 {
        result = blink(memo, 1, times-1);
    }
    else {
        let stone_str = stone.to_string();
        let stone_bytes = stone_str.as_bytes();
        if stone_bytes.len() % 2 == 0 {
            let lhs : &[u8] = &stone_bytes[0..(stone_bytes.len() / 2)];
            let rhs : &[u8] = &stone_bytes[(stone_bytes.len() / 2)..];
            let lhs_stone = String::from_utf8(lhs.to_vec()).expect("").parse::<u64>().expect("");
            let rhs_stone = String::from_utf8(rhs.to_vec()).expect("").parse::<u64>().expect("");

            result = blink(memo, lhs_stone, times-1) +
                blink(memo, rhs_stone, times-1);
        }
        else {
            let new_stone = stone * 2024;
            result = blink(memo, new_stone, times-1);
        }
    }
    memo.insert((stone, times), result);
    return result;
}

fn blink_all(memo: & mut HashMap<(u64, u64), u64>, stones : Vec<u64>, times : u64) -> u64 {
    let mut total = 0;
    for stone in stones {
        total += blink(memo, stone, times);
    }
    return total;
}

fn main() -> io::Result<()> {
    let args: Vec<String> = env::args().collect();
    let file_path = &args[1];
    let contents = fs::read_to_string(file_path)
        .expect("Should have been able to read the file");
    let numbers: Vec<u64> = contents.split_whitespace().map(|w| w.parse::<u64>().expect("Not a number")).collect();

    let mut memo : HashMap<(u64, u64), u64> = HashMap::new();
    println!("Solution 1: {:?}", blink_all(& mut memo, numbers.clone(), 25));
    println!("Solution 2: {:?}", blink_all(& mut memo, numbers.clone(), 75));

    Ok(())
}
