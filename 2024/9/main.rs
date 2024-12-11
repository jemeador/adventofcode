use std::env;
use std::io;
use std::fs;

#[derive(Debug)]
#[derive(Clone)]
struct Span {
    id : i64,
    size : u32,
}

fn main() -> io::Result<()> {
    let args: Vec<String> = env::args().collect();
    let file_path = &args[1];
    let contents = fs::read_to_string(file_path)
        .expect("Should have been able to read the file");
    let numbers: Vec<u32> = contents.chars().filter(|c| c.is_digit(10)).map(|c| c.to_digit(10).unwrap()).collect();


    let mut disk : Vec<i64> = Vec::new();
    let mut spans : Vec<Span> = Vec::new();

    for n in 0..numbers.len() {
        let used = n % 2 == 0;
        let size = numbers[n];
        let file_id = if used {(n as i64)/2} else {-1};
        for _d in 0..size {
            disk.push(file_id);
        }
        spans.push(Span {
            id: file_id,
            size: size,
        });
    }

    let mut j = disk.len() - 1;
    for d in 0..disk.len() {
        if disk[d] == -1 {
            while disk[j] == -1 {
                j -= 1;
            }
            if d >= j {
                break;
            }
            let temp = disk[d];
            disk[d] = disk[j];
            disk[j] = temp;
            j -= 1;
        }
    }

    let mut solution_1 : i64 = 0;

    for d in 0..disk.len() {
        if disk[d] == -1 {
            break;
        }
        solution_1 += disk[d] * (d as i64);
    }

    println!("Solution 1: {:?}", solution_1);

    let mut solution_2 : i64 = 0;
    let max_file_id = spans.len() as i64 / 2 + 1;
    for file_id in (0..max_file_id).rev() {
        let mut file_index = 0;
        let mut free_index = 0;
        let mut do_swap = false;
        for (span_index, span) in spans.clone().into_iter().enumerate() {
            if span.id == file_id {
                let file = span;
                for target_span_index in 0..spans.len() {
                    let target_span = &spans[target_span_index];
                    if target_span_index >= span_index {
                        break;
                    }
                    if target_span.id != -1 {
                        continue;
                    }
                    if target_span.size >= file.size {
                        do_swap = true;
                        free_index = target_span_index;
                        file_index = span_index;
                        break;
                    }
                }
                break;
            }
            file_index += 1;
        }
        if do_swap {
            let free_span = spans[free_index].clone();
            let file_span = spans[file_index].clone();
            // Move the block
            spans[free_index].size = 0;
            spans[file_index].id = -1;
            spans.insert(free_index, Span {
                id: -1,
                size: free_span.size - file_span.size,
            }); // Add a new free span
            spans.insert(free_index, file_span.clone()); // Insert before new free span
            // Add space to the free space before the removed segment
            //spans[file_index - 1].size += spans[file_index].size;
        }
    }

    let mut index = 0;
    for span in spans {
        if span.id == -1 {
            index += span.size;
            continue;
        }
        for _i in 0..span.size {
            solution_2 += span.id * (index as i64);
            println!("{:?} * {}", span.id , (index as i64));
            index += 1;
        }
    }

    println!("Solution 2: {}", solution_2);

    Ok(())
}
