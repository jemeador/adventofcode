use std::env;
use std::fs::File;
use std::io::{self, BufRead};

fn read_file_to_vec(file_path: &str) -> io::Result<Vec<Vec<char>>> {
    // Open the file
    let file = File::open(file_path)?;
    let reader = io::BufReader::new(file);

    // Read lines and collect into Vec<Vec<char>>
    let lines = reader.lines();
    let mut vec_of_vecs : Vec<Vec<char>> = Vec::new();
    for line in lines {
        let mut line_of_chars : Vec<char> = Vec::new();
        for character in line?.chars() {
            line_of_chars.push(character);
        }
        vec_of_vecs.push(line_of_chars);
    }
    Ok(vec_of_vecs)
}

fn width(grid: &Vec<Vec<char>>) -> isize {
    return grid[0].len() as isize;
}

fn height(grid: &Vec<Vec<char>>) -> isize {
    return grid.len() as isize;
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

fn xmas_search_dir(grid: &Vec<Vec<char>>, print_grid: &mut Vec<Vec<char>>, dir: (isize,isize)) -> i32 {
    let xmas = "XMAS";
    let mut ret = 0;
    for x in 0..width(grid) {
        for y in 0..height(grid) {
            let mut found_xmas = true;
            for i in 0..4 {
                let ix = x + i * dir.0;
                let iy = y + i * dir.1;
                if ix < 0 || ix >= width(grid) || iy < 0 || iy >= height(grid) {
                    found_xmas = false;
                    break;
                }
                if grid[iy as usize][ix as usize] != xmas.as_bytes()[i as usize] as char {
                    found_xmas = false;
                    break;
                }
            }
            if found_xmas {
                ret += 1;
                for i in 0..4 {
                    let ix = x + i * dir.0;
                    let iy = y + i * dir.1;
                    print_grid[iy as usize][ix as usize] = xmas.as_bytes()[i as usize] as char;
                }
            }
        }
    }
    return ret;
}

fn xmas_search(grid: &Vec<Vec<char>>) -> i32 {
    let mut empty_grid : Vec<Vec<char>> = grid.clone();
    for x in 0..width(grid) {
        for y in 0..height(grid) {
            empty_grid[y as usize][x as usize] = '.';
        }
    }
    let mut print_grid : Vec<Vec<char>> = empty_grid.clone();
    let mut count = 0;
    count += xmas_search_dir(grid, &mut print_grid, (1,0));
    count += xmas_search_dir(grid, &mut print_grid, (1,1));
    count += xmas_search_dir(grid, &mut print_grid, (0,1));
    count += xmas_search_dir(grid, &mut print_grid, (-1,1));
    count += xmas_search_dir(grid, &mut print_grid, (-1,0));
    count += xmas_search_dir(grid, &mut print_grid, (-1,-1));
    count += xmas_search_dir(grid, &mut print_grid, (0,-1));
    count += xmas_search_dir(grid, &mut print_grid, (1,-1));
    print(&print_grid);
    return count;
}

fn x_mas_search_dir(grid: &Vec<Vec<char>>, print_grid: &mut Vec<Vec<char>>, dir: [[isize; 2]; 2]) -> i32 {
    let mut ret = 0;
    for x in 0..width(grid) {
        for y in 0..height(grid) {
            if grid[y as usize][x as usize] != 'A' {
                continue;
            }
            let mut found_xmas = true;
            for d in dir.iter() {
                let ix = x + d[0];
                let iy = y + d[1];
                if ix < 0 || ix >= width(grid) || iy < 0 || iy >= height(grid) {
                    found_xmas = false;
                    break;
                }
                if grid[iy as usize][ix as usize] != 'M' {
                    found_xmas = false;
                    break;
                }
                let ix = x - d[0];
                let iy = y - d[1];
                if ix < 0 || ix >= width(grid) || iy < 0 || iy >= height(grid) {
                    found_xmas = false;
                    break;
                }
                if grid[iy as usize][ix as usize] != 'S' {
                    found_xmas = false;
                    break;
                }
            }
            if found_xmas {
                ret += 1;
                print_grid[y as usize][x as usize] = 'A';
                for d in dir.iter() {
                    let ix = x + d[0];
                    let iy = y + d[1];
                    print_grid[iy as usize][ix as usize] = 'M';
                    let ix = x - d[0];
                    let iy = y - d[1];
                    print_grid[iy as usize][ix as usize] = 'S';
                }
            }
        }
    }
    return ret;
}


fn x_mas_search(grid: &Vec<Vec<char>>) -> i32 {
    let mut empty_grid : Vec<Vec<char>> = grid.clone();
    for x in 0..width(grid) {
        for y in 0..height(grid) {
            empty_grid[y as usize][x as usize] = '.';
        }
    }
    let mut print_grid : Vec<Vec<char>> = empty_grid.clone();
    let mut count = 0;
    count += x_mas_search_dir(grid, &mut print_grid, [[-1,-1], [1,-1]]);
    count += x_mas_search_dir(grid, &mut print_grid, [[-1,-1], [-1,1]]);
    count += x_mas_search_dir(grid, &mut print_grid, [[-1,-1], [1,1]]);
    count += x_mas_search_dir(grid, &mut print_grid, [[1,-1], [-1,1]]);
    count += x_mas_search_dir(grid, &mut print_grid, [[1,-1], [1,1]]);
    count += x_mas_search_dir(grid, &mut print_grid, [[-1,1], [1,1]]);
    print(&print_grid);
    return count;
}

fn main() -> io::Result<()> {
    let args: Vec<String> = env::args().collect();
    let file_path = &args[1];
    let vec_of_vecs = read_file_to_vec(file_path)?;

    // Print the Vec<Vec<char>>
    println!("Solution 1: {}", xmas_search(&vec_of_vecs));

    println!("Solution 2: {}", x_mas_search(&vec_of_vecs));

    Ok(())
}
