use rand::{seq::SliceRandom, Rng};

#[repr(i8)]
#[derive(Clone, Copy, PartialEq)]
enum Fill {
    Searching = -1,
    Unknown = 0,
    Rock = 1,
    Steam = 2,
    Void = 3,
}

#[derive(Debug)]
struct C {
    pub x: usize,
    pub y: usize,
    pub z: usize,
}

impl C {
    pub fn new(l: &str, offset: usize) -> C {
        let spl: Vec<&str> = l.split(",").collect();
        C {
            x: spl[0].parse::<usize>().unwrap() + offset,
            y: spl[1].parse::<usize>().unwrap() + offset,
            z: spl[2].parse::<usize>().unwrap() + offset,
        }
    }
}

const SHAPE_PAD: usize = 2; // pad each edge so we don't index out of bounds, and so air has room to go around
const ARR_X: usize = SHAPE_PAD * 2 + 21;
const ARR_Y: usize = SHAPE_PAD * 2 + 20;
const ARR_Z: usize = SHAPE_PAD * 2 + 21;

type A = [[[Fill; ARR_Z]; ARR_Y]; ARR_X];
fn main() {
    let mut coords: Vec<C> = vec![];
    for l in std::fs::read_to_string("input").unwrap().lines() {
        coords.push(C::new(l, SHAPE_PAD));
    }
    // let x_max = coords.iter().map(|c| c.x).max().unwrap(); // 21
    // let y_max = coords.iter().map(|c| c.y).max().unwrap(); // 20
    // let z_max = coords.iter().map(|c| c.z).max().unwrap(); // 21

    let mut array: A = [[[Fill::Unknown; ARR_Z]; ARR_Y]; ARR_X];
    for c in &coords {
        array[c.x][c.y][c.z] = Fill::Rock;
    }

    part1(&array, &coords);
    part2(&mut array, &coords);
}

fn part1(array: &A, coords: &Vec<C>) {
    println!("Part1: {}", find_surface_area(array, coords, Fill::Unknown));
}

fn part2(array: &mut A, coords: &Vec<C>) {
    // For each point in the array, check if we can find the edge from there
    // If we find the edge, steam can reach all the points we walked to get there.
    // If we don't find the edge, it's probably void.
    let mut rng = rand::thread_rng();
    loop {
        let mut b = true;
        for z in 0..ARR_Z {
            for y in 0..ARR_Y {
                for x in 0..ARR_X {
                    let c = C { x, y, z };
                    if array[x][y][z] == Fill::Unknown {
                        do_search(array, &c, &mut rng);
                        b = false;
                    }
                }
            }
        }
        if b {
            break;
        }
    }

    println!("Part2: {}", find_surface_area(array, coords, Fill::Steam));
    // 2348 too low
    // 2370 too low? probably
    // 2447 wrong
    // 4279 wrong
}

fn do_search(array: &mut A, c: &C, rng: &mut rand::rngs::ThreadRng) {
    let mut ret = escape(array, c, 0, rng);
    match ret {
        Fill::Unknown => ret = Fill::Void,
        _ => (),
    }
    for z in 0..ARR_Z {
        for y in 0..ARR_Y {
            for x in 0..ARR_X {
                if array[x][y][z] == Fill::Searching {
                    array[x][y][z] = ret;
                }
            }
        }
    }
}

const MAX_DEPTH: i32 = 500;
fn escape(array: &mut A, c: &C, depth: i32, rng: &mut rand::rngs::ThreadRng) -> Fill {
    if array[c.x][c.y][c.z] == Fill::Searching {
        return Fill::Searching; // already here.
    }
    if array[c.x][c.y][c.z] == Fill::Rock {
        return Fill::Rock; // Can't search rock.
    }
    array[c.x][c.y][c.z] = Fill::Searching;
    if c.x == 0 || c.y == 0 || c.z == 0 {
        return Fill::Steam; // We touch the edge, everything walked can be reached by steam!
    }

    if depth > MAX_DEPTH {
        return Fill::Unknown;
    }
    let mut ret = Fill::Unknown;
    if c.x + 1 < ARR_X {
        let next = C {
            x: c.x + 1,
            y: c.y,
            z: c.z,
        };
        if escape(array, &next, depth + 1, rng) == Fill::Steam {
            ret = Fill::Steam;
        }
    }
    if c.y + 1 < ARR_Y {
        let next = C {
            x: c.x,
            y: c.y + 1,
            z: c.z,
        };
        if escape(array, &next, depth + 1, rng) == Fill::Steam {
            ret = Fill::Steam;
        }
    }
    if c.z + 1 < ARR_Z {
        let next = C {
            x: c.x,
            y: c.y,
            z: c.z + 1,
        };
        if escape(array, &next, depth + 1, rng) == Fill::Steam {
            ret = Fill::Steam;
        }
    }
    if c.x > 0 {
        let next = C {
            x: c.x - 1,
            y: c.y,
            z: c.z,
        };
        if escape(array, &next, depth + 1, rng) == Fill::Steam {
            ret = Fill::Steam;
        }
    }
    if c.y > 0 {
        let next = C {
            x: c.x,
            y: c.y - 1,
            z: c.z,
        };
        if escape(array, &next, depth + 1, rng) == Fill::Steam {
            ret = Fill::Steam;
        }
    }
    if c.z > 0 {
        let next = C {
            x: c.x,
            y: c.y,
            z: c.z - 1,
        };
        if escape(array, &next, depth + 1, rng) == Fill::Steam {
            ret = Fill::Steam;
        }
    }
    ret
}

fn find_surface_area(array: &A, coords: &Vec<C>, fill: Fill) -> i32 {
    let mut surface_area = 0;
    for c in coords {
        // check x-1, x+1
        if array[c.x - 1][c.y][c.z] == fill {
            surface_area += 1;
        }
        if array[c.x][c.y - 1][c.z] == fill {
            surface_area += 1;
        }
        if array[c.x][c.y][c.z - 1] == fill {
            surface_area += 1;
        }
        if array[c.x + 1][c.y][c.z] == fill {
            surface_area += 1;
        }
        if array[c.x][c.y + 1][c.z] == fill {
            surface_area += 1;
        }
        if array[c.x][c.y][c.z + 1] == fill {
            surface_area += 1;
        }
    }
    surface_area
}
