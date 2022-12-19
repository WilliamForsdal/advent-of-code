// 1 + 3 + 3 + 4 + 2

const SHAPE_WIDTH: usize = 7;
const SHAPE_HEIGHT: usize = 4;

#[derive(Clone, Copy)]
struct Shape {
    shape: [[u8; SHAPE_WIDTH]; SHAPE_HEIGHT],
}

impl Shape {
    pub fn new(shape: [[u8; 7]; 4]) -> Shape {
        Shape { shape }
    }

    pub fn col(&self, idx: usize) -> [u8; SHAPE_HEIGHT] {
        let s = self.shape;
        [s[0][0], s[0][1], s[0][2], s[0][3]]
    }

    pub fn print(&self) {
        for l in self.shape {
            for c in l {
                print!("{}")
            }
            println!("{l:?}");
        }
    }
}

fn main() {
    let contents =
        std::fs::read_to_string("day17.txt").expect("Should have been able to read the file");
    let mut pushes: Vec<i32> = vec![];
    for c in contents.chars() {
        match c {
            '<' => pushes.push(-1),
            '>' => pushes.push(1),
            _ => panic!("Woot"),
        }
    }
    part1(&pushes)
}

const CAVE_MAX_HEIGHT: usize = (1 + 3 + 3 + 4 + 2) * (2022 + 3) / 5 + 100; // add 100 for some margin above.
const CAVE_HEIGHT: usize = CAVE_MAX_HEIGHT;
const CAVE_WIDTH: usize = 7;

fn part1(pushes: &Vec<i32>) {
    let mut cave: [[u8; CAVE_WIDTH]; CAVE_HEIGHT] = [[0u8; CAVE_WIDTH]; CAVE_HEIGHT];
    let mut push_idx = 0;
    let mut highest_point = 0;

    for num_block in 0..2022 {
        // Spawn block
        let mut shape = get_shape(num_block % 5);
        let mut shape_y_offset = highest_point + 3; // spawn block 3 steps above last highest

        println!();
        loop {
            // push
            shape = push_shape(*(&pushes[push_idx]), &mut shape, &cave, shape_y_offset);

            push_idx += 1;
            if push_idx >= pushes.len() {
                push_idx = 0;
            }
            // if below is rock
            if !can_move(&shape, &cave, shape_y_offset, 0, -1) {
                for x in 0..SHAPE_WIDTH {
                    for y in 0..SHAPE_HEIGHT {
                        let cell = shape.shape[y][x];
                        if cell == 1 {
                            cave[y + shape_y_offset][x] = 1;
                            highest_point = y + shape_y_offset;
                        }
                    }
                }
                break;
            } else {
                // Move rock one step down and run loop again
                shape_y_offset -= 1;
            }
            break;
        }

        for y in (highest_point)..=0 {
            print!("|");
            for cell in cave[y] {
                if cell == 1 {
                    print!("#");
                } else {
                    print!(".");
                }
            }
            println!("|");
        }
    }

    println!("Part1: not done");
}

fn push_shape(
    push: i32,
    shape: &Shape,
    cave: &[[u8; 7]; CAVE_HEIGHT],
    shape_y_offset: usize,
) -> Shape {
    let mut clone_dst = shape.clone();
    // Check if the shape does not get pushed outside bounds
    if !can_move(shape, cave, shape_y_offset, push, 0) {
        return clone_dst; // Can't move right!
    }

    for x in 0..SHAPE_WIDTH {
        for y in 0..SHAPE_HEIGHT {
            let cx = x as i32 + push;
            if cx < 0 || cx >= SHAPE_WIDTH as i32 {
                continue;
            }
            clone_dst.shape[y][x] = shape.shape[y][cx as usize]
        }
    }
    clone_dst.print();
    clone_dst
}

fn can_move(
    shape: &Shape,
    cave: &[[u8; 7]; CAVE_HEIGHT],
    shape_y_offset: usize,
    xdiff: i32,
    ydiff: i32,
) -> bool {
    if (ydiff + shape_y_offset as i32) < 0 {
        return false;
    }

    if xdiff != 0 {
        let col = shape.col(0);
        for c in col {
            if c != 0 && xdiff < 0 {
                return false; // Cant move left
            }
        }
        let col = shape.col(SHAPE_WIDTH - 1);
        for c in col {
            if c != 0 && xdiff > 0 {
                return false; // Cant move right
            }
        }
    }

    for x in 0..SHAPE_WIDTH {
        for y in 0..SHAPE_HEIGHT {
            let cx = x as i32 + xdiff;
            let cy = y as i32 + ydiff + shape_y_offset as i32;
            if cx < 0
                || cx >= SHAPE_WIDTH as i32
                || x >= SHAPE_WIDTH
                || cy < 0
                || cy >= SHAPE_WIDTH as i32
            {
                continue;
            }
            let cx: usize = cx as usize;
            let cy: usize = cy as usize;

            let cave_cell = cave[cy][cx];
            let shape_cell = shape.shape[y][x];
            if shape_cell != 0 && cave_cell != 0 {
                return false;
            }
        }
    }
    return true;
}

fn get_shape(i: usize) -> Shape {
    const SHAPES: [[[u8; 7]; 4]; 5] = [
        [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 1, 1, 0],
        ],
        [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 1, 1, 1, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
        ],
        [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 1, 0, 0],
            [0, 0, 1, 1, 1, 0, 0],
        ],
        [
            [0, 0, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0],
        ],
        [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 0, 0, 0],
            [0, 0, 1, 1, 0, 0, 0],
        ],
    ];
    Shape::new(SHAPES[i])
}
