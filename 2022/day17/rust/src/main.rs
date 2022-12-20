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
        [s[0][idx], s[1][idx], s[2][idx], s[3][idx]]
    }

    pub fn print(&self) {
        for l in self.shape {
            for c in l {
                print!("{}", if c > 0 { "#" } else { "." });
            }
            println!("");
            // println!("{l:?}");
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
    // part1(&pushes, false);
    run(&pushes, true);
}

const CAVE_MAX_HEIGHT: usize = (1 + 3 + 3 + 4 + 2) * (2022 + 3) / 5;
const CAVE_HEIGHT: usize = CAVE_MAX_HEIGHT + 100; // add 100 for some margin above.
const CAVE_WIDTH: usize = 7;

fn run(pushes: &Vec<i32>, part2: bool) {
    let mut cave: [[u8; CAVE_WIDTH]; CAVE_HEIGHT] = [[0u8; CAVE_WIDTH]; CAVE_HEIGHT];
    let mut push_idx = 0;
    let mut highest_point = 0;

    let max = if part2 { 1000000000000 } else { 2022 };
    for num_block in 0..max {

        // Spawn block
        let mut shape = get_shape(num_block % 5);
        let mut shape_y_offset = highest_point + 3; // spawn block 3 steps above last highest

        // println!("Block starting at {shape_y_offset}");

        loop {
            // push
            // println!(
            //     "Pushing block number {num_block} to the {}.",
            //     if *(&pushes[(push_idx % pushes.len())]) > 0 {
            //         "right"
            //     } else {
            //         "left"
            //     }
            // );
            shape = push_shape(
                *(&pushes[(push_idx % pushes.len())]),
                &mut shape,
                &cave,
                shape_y_offset,
            );
            push_idx += 1;
            // if below is rock
            if !can_move(&shape, &cave, shape_y_offset, 0, -1) {
                // println!("The rock is coming to rest at {shape_y_offset}!");
                for (row_idx, row) in shape.shape.iter().enumerate() {
                    for (col_idx, cell) in row.iter().enumerate() {
                        if *cell == 1 {
                            cave[row_idx + shape_y_offset][col_idx] = 1;
                            if row_idx + shape_y_offset + 1 > highest_point {
                                highest_point = row_idx + shape_y_offset + 1; // Actaully 1 more than idx
                            }
                        }
                    }
                }
                break;
            } else {
                // Move rock one step down and run loop again
                shape_y_offset -= 1;
            }
        }

        // println!("After the rock comes to rest the shape_y_offset = {shape_y_offset}");
        // println!("The cave now looks like this:");
        // for row in (&cave[0..(highest_point + 3)]).iter().rev() {
        //     for c in row {
        //         if *c == 0 {
        //             print!(".")
        //         } else {
        //             print!("#");
        //         }
        //     }
        //     println!("");
        // }
        // println!("");
    }
    if part2 {
        println!("Part2: {}", highest_point);
    } else {
        println!("Part1: {highest_point}");
    }
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

    // println!("Clone before:");
    // clone_dst.print();

    for x in 0..SHAPE_WIDTH {
        for y in 0..SHAPE_HEIGHT {
            clone_dst.shape[y][x] = 0;
        }
    }

    for x in 0..SHAPE_WIDTH {
        for y in 0..SHAPE_HEIGHT {
            let cx = x as i32 + push;
            if cx >= 0 && cx < SHAPE_WIDTH as i32 {
                clone_dst.shape[y][cx as usize] = shape.shape[y][x];
            }
        }
    }
    // println!("Clone after:");
    // clone_dst.print();
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
        // Check if leftmost and rightmost edge of shape collides with walls
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

    for (row_idx, row) in shape.shape.iter().enumerate() {
        for (col_idx, cell) in row.iter().enumerate() {
            if ydiff != 0 {
                let y_below = row_idx as i32 + shape_y_offset as i32 - 1;

                if *cell == 1 && y_below < 0 {
                    return false; // The ground is below!
                }
                if y_below < 0 {
                    // We're checking underground but its ok
                    continue;
                }
                let cave_cell = cave[y_below as usize][col_idx];
                if cave_cell == 1 && *cell == 1 {
                    return false; // They would collide.
                }
            } else {
                let x_side = col_idx as i32 + xdiff;
                if x_side < 0 || x_side >= SHAPE_WIDTH as i32 {
                    continue;
                }
                let cave_cell = cave[(row_idx + shape_y_offset)][x_side as usize];
                if *cell == 1 && cave_cell == 1 {
                    // Collides with cave.
                    return false;
                }
            }
        }
    }

    return true;
}

fn get_shape(i: usize) -> Shape {
    const SHAPES: [[[u8; 7]; 4]; 5] = [
        [
            [0, 0, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
        ],
        [
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 1, 1, 1, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
        ],
        [
            [0, 0, 1, 1, 1, 0, 0],
            [0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
        ],
        [
            [0, 0, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0],
        ],
        [
            [0, 0, 1, 1, 0, 0, 0],
            [0, 0, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
        ],
    ];
    Shape::new(SHAPES[i])
}
