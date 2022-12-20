#[derive(Debug)]
struct C {
    pub x: usize,
    pub y: usize,
    pub z: usize,
}

impl C {
    pub fn new(l: &str) -> C {
        let spl: Vec<&str> = l.split(",").collect();
        C {
            x: spl[0].parse::<usize>().unwrap(),
            y: spl[1].parse::<usize>().unwrap(),
            z: spl[2].parse::<usize>().unwrap(),
        }
    }
}

fn main() {
    let mut coords: Vec<C> = vec![];
    for l in std::fs::read_to_string("input").unwrap().lines() {
        coords.push(C::new(l));
    }
    let x_max = coords.iter().map(|c| c.x).max().unwrap();
    let y_max = coords.iter().map(|c| c.y).max().unwrap();
    let z_max = coords.iter().map(|c| c.z).max().unwrap();
    println!("{x_max:?} {y_max:?} {z_max:?}");

    let mut array: [[[u8; 21 + 5]; 20 + 5]; 21 + 5] = [[[0u8; 21 + 5]; 20 + 5]; 21 + 5];
    for c in &coords {
        array[c.x][c.y][c.z] = 1;
    }
    let mut surface_area = 0;
    for c in &coords {
        // check x-1, x+1
        if c.x > 0 {
            if array[c.x - 1][c.y][c.z] == 0 {
                surface_area += 1;
            }
        } else {
            surface_area += 1;
        }
        if c.y > 0 {
            if array[c.x][c.y - 1][c.z] == 0 {
                surface_area += 1;
            }
        } else {
            surface_area += 1;
        }
        if c.z > 0 {
            if array[c.x][c.y][c.z - 1] == 0 {
                surface_area += 1;
            }
        } else {
            surface_area += 1;
        }
        if array[c.x + 1][c.y][c.z] == 0 {
            surface_area += 1;
        }
        if array[c.x][c.y + 1][c.z] == 0 {
            surface_area += 1;
        }
        if array[c.x][c.y][c.z + 1] == 0 {
            surface_area += 1;
        }
    }

    println!("Part1: {surface_area}");
    // 4632 too low.
}
