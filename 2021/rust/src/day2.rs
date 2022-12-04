use std::fs::File;
use std::io::prelude::*;

pub fn f() {
    part2();
}

fn part1() {
    let file = File::open("./input2").expect("Failed to open file.");
    let reader = std::io::BufReader::new(file);

    let mut up_down = 0;
    let mut fw_bw = 0;
    for line in reader.lines()
    {
        let line = line.unwrap();
        let split = line.split(" ");
        let vec = split.collect::<Vec<&str>>();
        let direction = vec[0].trim();
        let distance = vec[1].trim();
        let distance:i32 = distance.parse().unwrap();

        match direction
        {
            "down" => up_down += distance,
            "up" => up_down -= distance,
            "forward" => fw_bw += distance,
            "backward" => fw_bw -= distance,
            _ => println!("ERROR"),
        };
    }
    println!("depth: {}, distance: {}", up_down, fw_bw);

    println!("product: {}", up_down * fw_bw);

}

fn part2() {
    let file = File::open("./input2").expect("Failed to open file.");
    let reader = std::io::BufReader::new(file);

    let mut up_down = 0;
    let mut aim = 0;
    let mut fw_bw = 0;
    for line in reader.lines()
    {
        let line = line.unwrap();
        let split = line.split(" ");
        let vec = split.collect::<Vec<&str>>();
        let direction = vec[0].trim();
        let distance = vec[1].trim();
        let value:i32 = distance.parse().unwrap();

        match direction
        {
            "down" => aim += value,
            "up" => aim -= value,
            "forward" => {
                fw_bw += value;
                up_down += aim * value;
            },
            "backward" => {
                fw_bw -= value;
                up_down += aim * value;
            }
            _ => println!("ERROR"),
        };
    }
    println!("depth: {}, distance: {}", up_down, fw_bw);
    println!("product: {}", up_down * fw_bw);
}