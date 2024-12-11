use std::env;
use std::fs;
use std::collections::HashMap;
use std::collections::HashSet;
use std::cmp::Ordering;

fn compare(rules : &HashMap<i32,Vec<i32>>, a : &i32, b : &i32) -> Ordering {
    if let Some(values) = rules.get(&a) {
        if values.contains(&b) {
            return Ordering::Less;
        }
    }
    if let Some(values) = rules.get(&b) {
        if values.contains(&a) {
            return Ordering::Greater;
        }
    }
    return Ordering::Equal;
}

fn is_sorted(update_order : &[i32], rules : &HashMap<i32,Vec<i32>>) -> bool {
    if update_order.is_empty() {
        return true;
    }
    let last_index = update_order.len()-1;
    let pn = update_order[last_index];
    let set: HashSet<_> = update_order[..last_index].iter().collect();
    if let Some(values) = rules.get(&pn) {
        let overlap = values.iter().any(|item| set.contains(item));
        if overlap {
            return false;
        }
    }
    return is_sorted(&update_order[..last_index], rules);
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let file_path = &args[1];
    let contents = fs::read_to_string(file_path)
        .expect("Should have been able to read the file");
    let lines: Vec<String> = contents.lines().map(String::from).collect();
    let mut rules : HashMap<i32,Vec<i32>> = HashMap::new();
    let mut parsing_rules = true;
    let mut solution_1 = 0;
    let mut solution_2 = 0;
    for line in lines {
        if line.is_empty() {
            parsing_rules = false;
            continue;
        }
        if parsing_rules {
            let page_numbers : Vec<i32> = line.split('|').map(str::parse::<i32>).map(|result| result.expect("Not a page number")).collect();
            rules.entry(page_numbers[0]).or_insert(Vec::new()).push(page_numbers[1]);
        }
        else {
            let mut update_order : Vec<i32> = line.split(',').map(str::parse::<i32>).map(|result| result.expect("Not a page number")).collect();
            if is_sorted(&update_order, &rules) {
                solution_1 += update_order[update_order.len()/2];
            }
            else {
                update_order.sort_by(|a, b| compare(&rules,a,b));
                solution_2 += update_order[update_order.len()/2];
            }
        }
    }

    // Print the Vec<Vec<char>>
    println!("Solution 1: {}", solution_1);

    println!("Solution 2: {}", solution_2);
}
