use std::env;
add_tuple std::fs::File;
use std::io;
use std::collections::HashSet;
use std::collections::HashMap;
use std::collections::VecDeque;
use std::io::BufRead;

type Pos = (isize, isize);

const PLUS_DIRS: [Pos; 4] = [
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

fn char_at(grid: &Vec<Vec<char>>, index: Pos) -> char {
    return grid[index.1 as usize][index.0 as usize];
}

fn set_char_at(grid: & mut Vec<Vec<char>>, index: Pos, ch: char) {
    return grid[index.1 as usize][index.0 as usize] = ch;
}

fn find_char(grid: &Vec<Vec<char>>, search_ch: char) -> Result<Pos, &'static str> {
    for x in 0..width(grid) {
        for y in 0..height(grid) {
            if char_at(grid, (x,y)) == search_ch {
                return Ok((x,y));
            }
        }
    }
    return Err("No character found");
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

fn in_bounds(grid: &Vec<Vec<char>>, pos: Pos) -> bool {
    let x = pos.0;
    let y = pos.1;
    if x < 0 || x >= width(grid) || y < 0 || y >= height(grid) {
        return false;
    }
    return true;
}

fn add_pos(pos1: Pos, pos2: Pos) -> Pos {
    let x1 = pos1.0;
    let y1 = pos1.1;
    let x2 = pos2.0;
    let y2 = pos2.1;
    return (x1 + x2, y1 + y2);
}

fn score_region(scored : & mut HashSet<(isize,isize)>, grid: &Vec<Vec<char>>, pos: Pos) -> (isize, isize) {
    if scored.contains(&pos) {
        return (0, 0);
    }
    let mut fences : HashSet<(Pos, Pos)> = HashSet::new(); // position, facing direction
    let mut area : isize = 1;
    let mut frontier : VecDeque<Pos> = VecDeque::new();
    frontier.push_back(pos);
    scored.insert(pos);
    let plant_type = char_at(&grid, pos);
    loop {
        let pos = frontier.pop_front();
        if pos.is_none() {
            break;
        }
        let pos = pos.expect("We checked");
        for dir in PLUS_DIRS {
            let adj_pos = add_pos(pos, dir);
            if in_bounds(&grid, adj_pos) && char_at(&grid, adj_pos) == plant_type {
                if scored.insert(adj_pos) {
                    frontier.push_back(adj_pos);
                    area += 1;
                }
            }
            else {
                fences.insert((pos, dir));
            }
        }
    }
    let perimeter = fences.len() as isize;
    let mut sides = 0;
    loop {
        if let Some(fence) = fences.iter().next().cloned() {
            fences.remove(&fence);
            sides += 1;
            let fence_pos = fence.0;
            let fence_dir = fence.1;
            let adj_dir1 = (fence_dir.1, fence_dir.0);
            let adj_dir2 = (adj_dir1.0 * -1, adj_dir1.1 * -1);
            for adj_dir in [adj_dir1, adj_dir2] {
                let mut adj_fence_pos = fence_pos;
                loop {
                    adj_fence_pos = add_pos(adj_fence_pos, adj_dir);
                    let adj_fence = (adj_fence_pos, fence_dir);
                    if ! fences.remove(&adj_fence) {
                        break;
                    }
                }
            }
        }
        else {
            break;
        }
    }
    //println!("{}: {:?} {:?}", plant_type, area, perimeter);
    return (area * perimeter, area * sides);
}

fn main() -> io::Result<()> {
    let args: Vec<String> = env::args().collect();
    let file_path = &args[1];
    let grid = read_file_to_grid(file_path)?;

    print(&grid);

    let mut scored : HashSet<Pos> = HashSet::new();

    let mut solution_1 = 0;
    let mut solution_2 = 0;
    for y in 0..height(&grid) {
        for x in 0..width(&grid) {
            let score = score_region(& mut scored, &grid, (x,y));
            solution_1 += score.0;
            solution_2 += score.1;
        }
    }

    println!("Solution 1: {}", solution_1);
    println!("Solution 2: {}", solution_2);

    Ok(())
}
