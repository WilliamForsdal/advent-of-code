use core::num;
use std::{fs, task::Context};

// 1 + 3 + 3 + 4 + 2
const MAX_HEIGHT: u32 = (1 + 3 + 3 + 4 + 2) * (2022+3) / 5; // 2022 + 3 to round up

enum Push {
    Left,
    Right,
}

fn main() {
    // println!("Max height: {MAX_HEIGHT}");
    let contents = fs::read_to_string("day17.txt").expect("Should have been able to read the file");
    let mut pushes: Vec<Push> = vec![];
    for c in contents.chars() {
        match c {
            '<' => pushes.push(Push::Left),
            '>' => pushes.push(Push::Right),
            _ => panic!("Woot"),
        }
    }
    part1(&pushes)
}

fn part1(pushes: &Vec<Push>) {
    let mut arr: [[u8;7]; MAX_HEIGHT] = [[0u8;7]; MAX_HEIGHT]
    let mut num_blocks = 0;
    let mut push_ptr =  0;
    while num_blocks < 2022 {

        // Spawn block
        // push
        // if below is not rock, move down
        // Else 


        num_blocks += 1;
    }
    
    println!("Part1: not done");

    fn a() {

    }
}
