use std::fs::File;
use std::io::prelude::*;

pub fn d1() {

    let file = File::open("./input").expect("Failed to open file.");
    let mut reader = std::io::BufReader::new(file);
    part1(&mut reader);
    reader.rewind().expect("Failed to rewind.");
    part2(&mut reader);
}

fn part1(reader: &mut std::io::BufReader<File>)
{
    let mut bigger: i32 = -1;
    let mut prev: i32 = 0;
    for line in reader.lines()
    {
        let val:i32 = line.unwrap().parse().unwrap();
        if val > prev {
            bigger += 1;
        }
        prev = val;
    }
    println!("part 1 result: {}", bigger);
}

fn part2(reader: &mut std::io::BufReader<File>)
{
    let mut x0: i32 = 0;
    let mut x1: i32 = 0;
    let mut x2: i32 = 0;
    let mut c3: i32 = 3;
    let mut prev_sum: i32 = 0;
    let mut count: i32 = -1;
    for line in reader.lines()
    {
        x0 = x1;
        x1 = x2;
        x2 = line.unwrap().parse().unwrap();
        if c3 == 0
        {
            let sum: i32 = x0+x1+x2;
            if sum > prev_sum
            {
                count += 1;
            }
            prev_sum = sum;
        } 
        else {
            c3 -= 1;
        }
    }
    println!("part 2 result: {}", count);
}