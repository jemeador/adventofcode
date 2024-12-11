use std::env;
use std::fs::File;
use std::io;
use std::collections::HashSet;
use std::collections::HashMap;
use std::collections::VecDeque;
use std::io::BufRead;

const PLUS_DIRS: [(isize, isize); 4] = [
    (0,-1),
    (1,0),
    (0,1),
    (-1,0),
];

fn read_file_to_grid(file_path: &str) -> io::Result<Vec<Vec<char>>> {
    // Open the file
    let file = File::open(file_path)?;
    let reader = io::BufReader::new(file);

    // Read lines and collect into Vec<Vec<char>>
    let lines = reader.lines();
    let mut grid : Vec<Vec<char>> = Vec::new();
    for line in lines {
        let mut line_of_chars : Vec<char> = Vec::new();
        for character in line?.chars() {
            line_of_chars.push(character);
        }
        grid.push(line_of_chars);
    }
    Ok(grid)
}

fn width(grid: &Vec<Vec<char>>) -> isize {
    return grid[0].len() as isize;
}

fn height(grid: &Vec<Vec<char>>) -> isize {
    return grid.len() as isize;
}

fn char_at(grid: &Vec<Vec<char>>, index: (isize, isize)) -> char {
    return grid[index.1 as usize][index.0 as usize];
}

fn set_char_at(grid: & mut Vec<Vec<char>>, index: (isize, isize), ch: char) {
    return grid[index.1 as usize][index.0 as usize] = ch;
}

fn find_chars(grid: &Vec<Vec<char>>, search_ch: char) -> Vec<(isize, isize)> {
    let mut ret : Vec<(isize, isize)> = Vec::new();
    for x in 0..width(grid) {
        for y in 0..height(grid) {
            if char_at(grid, (x,y)) == search_ch {
                ret.push((x,y));
            }
        }
    }
    return ret;
}

fn print(grid: &Vec<Vec<char>>) {
    for line in grid {
        for ch in line {
            print!("{}", ch);
        }
        println!();
    }
    println!();
}

fn in_bounds(grid: &Vec<Vec<char>>, pos: (isize, isize)) -> bool {
    let x = pos.0;
    let y = pos.1;
    if x < 0 || x >= width(grid) || y < 0 || y >= height(grid) {
        return false;
    }
    return true;
}

fn add_pos(pos1: (isize, isize), pos2: (isize, isize)) -> (isize, isize) {
    let x1 = pos1.0;
    let y1 = pos1.1;
    let x2 = pos2.0;
    let y2 = pos2.1;
    return (x1 + x2, y1 + y2);
}

fn get_trailhead_score(grid: &Vec<Vec<char>>, start: (isize, isize), part2: bool) -> isize {
    let mut score : isize = 0;
    let mut visited : HashSet<(isize, isize)> = HashSet::new();
    let mut frontier : VecDeque<(isize, isize)> = VecDeque::new();
    let mut distinct_paths : HashMap<(isize, isize), isize> = HashMap::new();
    frontier.push_back(start);
    while let pos = frontier.pop_front() {
        if pos.is_none() {
            break;
        }
        let pos = pos.expect("Checked if not none");
        let height = char_at(&grid, pos).to_digit(10).expect("Not a digit");
        let path_count = *distinct_paths.entry(pos).or_insert(1);
        if height == 9 {
            if part2 {
                score += path_count;
            }
            else {
                score += 1;
            }
            continue;
        }
        for dir in PLUS_DIRS {
            let adj_pos = add_pos(pos, dir);
            if in_bounds(&grid, adj_pos) &&
                char::from_digit(height+1,10) == Some(char_at(&grid, adj_pos)) {
                if visited.insert(adj_pos) {
                    frontier.push_back(adj_pos);
                }
                *distinct_paths.entry(adj_pos).or_insert(0) += path_count;
            }
        }
    }
    return score;
}

fn main() -> io::Result<()> {
    let args: Vec<String> = env::args().collect();
    let file_path = &args[1];
    let grid = read_file_to_grid(file_path)?;

    print(&grid);

    let mut solution_1 = 0;

    for start in find_chars(&grid, '0') {
        solution_1 += get_trailhead_score(&grid, start, false);
    }

    println!("Solution 1: {}", solution_1);

    let mut solution_2 = 0;
    for start in find_chars(&grid, '0') {
        solution_2 += get_trailhead_score(&grid, start, true);
    }

    println!("Solution 2: {}", solution_2);

    Ok(())
}
