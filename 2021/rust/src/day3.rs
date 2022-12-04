use std::clone;
use std::fs::File;
use std::io::BufReader;
use std::io::prelude::*;
use std::collections::HashMap;


pub fn f()
{
    part1();
    part2();
}

fn part1() {
    let file = File::open("./d3").expect("Failed to open file.");
    let reader = BufReader::new(file);
    // 010011001001
    let mut bit_counts: HashMap<i32, i32> = HashMap::new();
    let mut tot: i32 = 0;

    for line in reader.lines()
    {
        tot += 1;
        let mut index: i32 = 0;
        for ch in line.unwrap().chars()
        {
            if !bit_counts.contains_key(&index)
            {
                bit_counts.insert(index, 0);
            }
            match ch {
                '0' => (),
                '1' => {bit_counts.insert(index, bit_counts.get(&index).unwrap() + 1);},
                _ => ()
            }
            index += 1;
        }
    }
    
    let half:i32 = tot/2;
    let mut gamma: u32 = 0;
    let mut epsilon: u32 = 0;

    for i in 0..12
    {
        let num_bits_at_index = bit_counts.get(&i).unwrap();
        if num_bits_at_index > &half
        {
            gamma |= 1 << (11-i);
        }
        else {
            epsilon |= 1 << (11-i);
        }
    }
    println!("Gamma: {}", gamma);
    println!("Epsilon: {}", epsilon);
    println!("result: {}", gamma * epsilon);
}


fn part2() 
{
    let file = File::open("./d3").expect("Failed to open file.");
    let reader = BufReader::new(file);

    let mut ones: Vec<u16> = Vec::new();

    for line in reader.lines()
    {
        let l = line.unwrap();
        ones.push(u16::from_str_radix(&l, 2).unwrap());
    }
    let mut zeroes = ones.clone();
    let mut char_idx = 12;
    loop {
        let mut fucker = 0;
        for line in &mut zeroes {
            if line & 0x01 << char_idx > 0 {
                zeroes.remove(fucker);
                fucker += 1;
            }
        }

        if zeroes.len() == 1 {
            break;
        }
        char_idx -= 1;
    }
    
    println!("{}", zeroes[0]);

} 

struct CC {
    pub c: u32
}

impl CC {
    pub fn new() -> CC {
        CC {c: 0}
    }
}

// let line = line.unwrap();
// let mut iter = 0;
// for c in line.chars() {
//     match c {
//         '0' => zeroes[iter] += 1,
//         '1' => ones[iter] += 1,
//         _ => panic!()
//     };
//     iter += 1;
// }
// println!("");
// println!("{}", line);