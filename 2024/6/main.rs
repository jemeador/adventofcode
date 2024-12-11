use std::env;
use std::fs::File;
use std::io;
use std::collections::HashSet;
use std::io::BufRead;

fn read_file_to_vec(file_path: &str) -> io::Result<Vec<Vec<char>>> {
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

fn find_char(grid: &Vec<Vec<char>>, search_ch: char) -> Result<(isize, isize), &'static str> {
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

fn travel(grid: &Vec<Vec<char>>) -> Result<i32, &'static str> {
    let dirs = [
        (0,-1),
        (1,0),
        (0,1),
        (-1,0),
    ];

    let mut print_grid = grid.clone();
    let mut visited_states : HashSet<(isize, isize, i8)> = HashSet::new();
    let start = find_char(&grid, '^');
    let mut d = 0;
    let mut pos = start.expect("Could not find ^");
    let mut cells_visited = 0;

    loop {
        if char_at(&print_grid, pos) != 'X' {
            set_char_at(& mut print_grid, pos, 'X');
            cells_visited += 1;
        }
        let state = (pos.0, pos.1, d);
        if visited_states.contains(&state) {
            return Err("Infinite loop");
        }
        //let possible_future_state = (pos.0, pos.1, (d + 1) % 4);
        //if visited_states.contains(&possible_future_state) {
        //    println!("Found block site {:?}", possible_future_state)
        //}
        visited_states.insert(state);
        let mut next_pos = add_pos(pos, dirs[d as usize]);
        if !in_bounds(&grid, next_pos) {
            break;
        }
        while char_at(&grid, next_pos) == '#' {
            d = (d + 1) % 4;
            next_pos = add_pos(pos, dirs[d as usize]);
        }
        pos = next_pos;
    }

    //print(&print_grid);
    return Ok(cells_visited);
}

fn main() -> io::Result<()> {
    let args: Vec<String> = env::args().collect();
    let file_path = &args[1];
    let grid = read_file_to_vec(file_path)?;

    println!("Solution 1: {}", travel(&grid).expect("No solution 1"));

    let mut solution_2 = 0;

    let start = find_char(&grid, '^');
    for x in 0..width(&grid) {
        for y in 0..height(&grid) {
            if (x, y) != start.expect("Could not find ^") {
                let mut modified_grid = grid.clone();
                set_char_at(& mut modified_grid, (x, y), '#');
                if travel(&modified_grid).is_err() {
                    println!("{:?}", (x,y));
                    solution_2 += 1;
                }
            }
        }
    }

    println!("Solution 2: {}", solution_2);

    Ok(())
}
