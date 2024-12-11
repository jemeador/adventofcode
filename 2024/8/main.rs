use std::env;
use std::fs::File;
use std::io;
use std::collections::HashMap;
use std::collections::HashSet;
use std::io::BufRead;

/*
const PLUS_DIRS: [(i32, i32); 4] = [
    (0,-1),
    (1,0),
    (0,1),
    (-1,0),
];
*/

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

/*
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
*/

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

fn sub_pos(pos1: (isize, isize), pos2: (isize, isize)) -> (isize, isize) {
    let x1 = pos1.0;
    let y1 = pos1.1;
    let x2 = pos2.0;
    let y2 = pos2.1;
    return (x1 - x2, y1 - y2);
}

fn main() -> io::Result<()> {
    let args: Vec<String> = env::args().collect();
    let file_path = &args[1];
    let grid = read_file_to_grid(file_path)?;
    let mut print_grid = grid.clone();
    let mut print_grid_2 = grid.clone();

    //print(&grid);

    let mut antennas : HashMap<char, Vec<(isize,isize)>> = HashMap::new();

    for x in 0..width(&grid) {
        for y in 0..height(&grid) {
            let frequency = char_at(&grid, (x,y));
            if frequency != '.' {
                antennas.entry(frequency).or_default().push((x,y));
            }
        }
    }

    let mut antinodes_part_1 : HashSet<(isize, isize)> = HashSet::new();
    let mut antinodes_part_2 : HashSet<(isize, isize)> = HashSet::new();

    for (_a,positions) in antennas {
        for i in 0..positions.len() {
            for j in 0..positions.len() {
                if i == j {
                    continue;
                }
                let pos1 = positions[i];
                let pos2 = positions[j];
                // Part 1
                let antinode1 = add_pos(pos2, sub_pos(pos2, pos1));
                let antinode2 = add_pos(pos1, sub_pos(pos1, pos2));
                if in_bounds(&grid, antinode1) {
                    antinodes_part_1.insert(antinode1);
                    set_char_at(& mut print_grid, antinode1, '#');
                }
                if in_bounds(&grid, antinode2) {
                    antinodes_part_1.insert(antinode2);
                    set_char_at(& mut print_grid, antinode2, '#');
                }
                // Part 2
                let mut offset = sub_pos(pos2, pos1);
                for p in 2..height(&grid) {
                    // Poor man's prime factorization
                    while offset.0 % p == 0 && offset.1 % p == 0 {
                        offset.0 /= p;
                        offset.1 /= p;
                    }
                }
                let mut pos = pos1;
                while in_bounds(&grid, pos) {
                    antinodes_part_2.insert(pos);
                    set_char_at(& mut print_grid_2, pos, '#');
                    pos = add_pos(pos, offset);
                }
                pos = pos1;
                while in_bounds(&grid, pos) {
                    antinodes_part_2.insert(pos);
                    set_char_at(& mut print_grid_2, pos, '#');
                    pos = sub_pos(pos, offset);
                }
            }
        }
    }

    print(&print_grid);
    println!("Solution 1: {}", antinodes_part_1.len());
    print(&print_grid_2);
    println!("Solution 2: {}", antinodes_part_2.len());

    Ok(())
}
