use std::env;
use std::io;
use std::collections::HashSet;
use std::fs;
extern crate geo;
extern crate line_intersection;

type Pos = (isize, isize);

/*
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400
*/
fn add_pos(pos1: Pos, pos2: Pos) -> Pos {
    let x1 = pos1.0;
    let y1 = pos1.1;
    let x2 = pos2.0;
    let y2 = pos2.1;
    return (x1 + x2, y1 + y2);
}

fn parse_button_line(line : &String) -> Pos {
    let x0 = line.find('+').expect("") + 1;
    let x1 = line.find(',').expect("");
    let y0 = line[x1..].find('+').expect("") + 1;
    let x = line[x0..x1].parse().expect("");
    let y = line[x1+y0..].parse().expect("");
    return (x, y);
}
fn parse_prize_line(line : &String) -> Pos {
    let x0 = line.find('=').expect("") + 1;
    let x1 = line.find(',').expect("");
    let y0 = line[x1..].find('=').expect("") + 1;
    let x = line[x0..x1].parse().expect("");
    let y = line[x1+y0..].parse().expect("");
    return (x, y);
}

fn main() -> io::Result<()> {
    let args: Vec<String> = env::args().collect();
    let file_path = &args[1];

    let contents = fs::read_to_string(file_path)
        .expect("Should have been able to read the file");

    let mut groups : Vec<(Pos, Pos, Pos)> = Vec::new();
    let mut group_used_1 : HashSet<(Pos, Pos, Pos)> = HashSet::new();
    let mut group_used_2 : HashSet<(Pos, Pos, Pos)> = HashSet::new();

    for machine_str in contents.split("\n\n") {
        let lines: Vec<String> = machine_str.lines().map(String::from).collect();
        let a = parse_button_line(&lines[0]);
        let b = parse_button_line(&lines[1]);
        let p = parse_prize_line(&lines[2]);
        groups.push((a,b,p));
    }

    let mut solution_1 = 0;
    for group in &groups {
        let (a, b, p) = group;

        for i in 0..100 {
            let mut pos = (0,0);
            for _ in 0..i {
                pos = add_pos(pos, *a);
            }
            let mut j = 0;
            loop {
                if pos.0 > p.0 || pos.1 > p.1 {
                    break;
                }
                if pos.0 == p.0 && pos.1 == p.1 {
                    solution_1 += i * 3 + j * 1;
                    group_used_1.insert(*group);
                    break;
                }
                pos = add_pos(pos, *b);
                j += 1;
            }
        }
    }

    println!("Solution 1: {}", solution_1);

    let mut solution_2 = 0;
    for group in groups {
        let (a, b, p) = group;
        let p = (p.0 + 10000000000000, p.1 + 10000000000000);
        //println!("{:?} {:?} {:?}", a, b, p);
        use geo::Line;
        use line_intersection::LineInterval;
        let line1 = LineInterval::line(Line::<f64> {
            start: (0.0, 0.0).into(),
            end: (a.0 as f64, a.1 as f64).into(),
        });
        let line2 = LineInterval::line(Line::<f64> {
            start: (p.0 as f64, p.1 as f64).into(),
            end: ((p.0 + b.0) as f64, (p.1 + b.1) as f64).into(),
        });

        let intersection = line1.relate(&line2).unique_intersection().expect("");
        //println!("{:?}", intersection);
        //println!("{:?} == {:?}", intersection.x().round(), intersection.x());
        //println!("{:?} == {:?}", intersection.y().round(), intersection.y());
        let intersection = intersection.x().round() as isize;
        let a_presses = (intersection / a.0);
        let b_presses = (p.0 - intersection) / b.0;
        // Test that we can hit the prize exactly with a discrete number of button presses. This
        // gets around the issue with floating point precision.
        let x_proof = a_presses * a.0 + b_presses * b.0;
        let y_proof = a_presses * a.1 + b_presses * b.1;
        if ((x_proof, y_proof) == p) {
            solution_2 +=  a_presses * 3 + b_presses;
            group_used_2.insert(group);
        }
    }

    println!("{:?}", group_used_1.difference(&group_used_2));

    println!("Solution 2: {}", solution_2);

    Ok(())
}
