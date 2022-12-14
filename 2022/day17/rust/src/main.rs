// 1 + 3 + 3 + 4 + 2
const CAVE_MAX_HEIGHT: usize = (1 + 3 + 3 + 4 + 2) * (2022 + 3) / 5;
const CAVE_HEIGHT: usize = CAVE_MAX_HEIGHT + 20000; // add some margin above.
const CAVE_WIDTH: usize = 7;

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

    fn push(&mut self, push: i32, simulation: &Simulation, shape_y_offset: usize) {
        let copy = self.clone();
        // Check if the shape does not get pushed outside bounds
        if !simulation.can_move(self, shape_y_offset, push, 0) {
            return; // Can't move right!
        }

        for y in 0..SHAPE_HEIGHT {
            for x in 0..SHAPE_WIDTH {
                self.shape[y][x] = 0;
            }
        }

        for y in 0..SHAPE_HEIGHT {
            for x in 0..SHAPE_WIDTH {
                let cx = x as i32 + push;
                if copy.shape[y][x] == 1 {
                    if cx >= 0 && cx < SHAPE_WIDTH as i32 {
                        self.shape[y][cx as usize] = 1;
                    }
                }
            }
        }
    }
}

struct Simulation {
    pub highest_point: usize,
    pub cave: [[u8; CAVE_WIDTH]; CAVE_HEIGHT],
    pub step: usize,
    pub push_idx: usize,
    pushes: Vec<i8>,
}

impl Simulation {
    pub fn new(pushes: Vec<i8>) -> Simulation {
        Simulation {
            highest_point: 0,
            cave: [[0u8; CAVE_WIDTH]; CAVE_HEIGHT],
            step: 0,
            push_idx: 0,
            pushes,
        }
    }

    fn print_cave(&self, idx: usize, len: usize) {
        println!("The cave now looks like this:");

        for r in (idx..idx + len).rev() {
            if r >= self.cave.len() {
                continue;
            }
            print!("row {r:5}: ");
            for c in self.cave[r] {
                if c == 0 {
                    print!(".")
                } else {
                    print!("#");
                }
            }
            println!("");
        }
        println!("");
    }

    fn step(&mut self) {
        // Spawn block
        let mut shape = Shape::get_shape(self.step % 5);
        let mut shape_y_offset = self.highest_point + 3 + 1; // spawn block 3 steps above last highest, ie + 1
        if self.step == 0 {
            shape_y_offset = 3;
        }
        // shape.print();

        loop {
            shape.push(
                (self.pushes[(self.push_idx % self.pushes.len())]) as i32,
                &self,
                shape_y_offset,
            );
            self.push_idx += 1;
            // if below is rock
            if !self.can_move(&shape, shape_y_offset, 0, -1) {
                for (row_idx, row) in shape.shape.iter().enumerate() {
                    for (col_idx, cell) in row.iter().enumerate() {
                        if *cell == 1 {
                            self.cave[row_idx + shape_y_offset][col_idx] = 1;
                            if row_idx + shape_y_offset > self.highest_point {
                                self.highest_point = row_idx + shape_y_offset;
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
        self.step += 1;
    }

    fn can_move(&self, shape: &Shape, shape_y_offset: usize, xdiff: i32, ydiff: i32) -> bool {
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
                    let cave_cell = self.cave[y_below as usize][col_idx];
                    if cave_cell == 1 && *cell == 1 {
                        return false; // They would collide.
                    }
                } else {
                    let x_side = col_idx as i32 + xdiff;
                    if x_side < 0 || x_side >= SHAPE_WIDTH as i32 {
                        continue;
                    }
                    let cave_cell = self.cave[(row_idx + shape_y_offset)][x_side as usize];
                    if *cell == 1 && cave_cell == 1 {
                        // Collides with cave.
                        return false;
                    }
                }
            }
        }

        return true;
    }
}

fn main() {
    let contents =
        std::fs::read_to_string("day17.txt").expect("Should have been able to read the file");
    let mut pushes: Vec<i8> = vec![];
    for c in contents.chars() {
        match c {
            '<' => pushes.push(-1),
            '>' => pushes.push(1),
            _ => panic!("Woot"),
        }
    }
    part1(pushes.clone());
    part2(pushes.clone());
    // part2(&pushes);
}
fn part1(pushes: Vec<i8>) {
    let mut sim = Simulation::new(pushes);
    for _step in 0..2022 {
        sim.step();
    }
    // highest_point + 1 because highest_point is an index.
    println!("Part1: {}", sim.highest_point + 1);
}

fn part2(pushes: Vec<i8>) {
    let mut sim = Simulation::new(pushes.clone());
    let mut total_height = 0;

    for _ in 0..2022 {
        sim.step();
    }
    println!("Part1: {}", sim.highest_point + 1);

    for _ in 0..10000 {
        sim.step();
    }

    let mut cycle_start_idx = 0;
    let mut cycle_start_row = None;
    let mut height_per_cycle = 0;
    let mut steps_per_cycle = 0;
    let mut found = false;

    loop {
        if found {
            break;
        }
        sim.step();

        for r1_idx in 0..sim.highest_point {
            for r2_idx in (r1_idx + 100)..sim.highest_point {
                if sim.cave[r1_idx] == sim.cave[r2_idx] {
                    let mut r1_idx_i = r1_idx + 1;
                    let mut r2_idx_i = r2_idx + 1;
                    let mut diff = 0;
                    while sim.cave[r1_idx_i] == sim.cave[r2_idx_i] {
                        r1_idx_i += 1;
                        r2_idx_i += 1;
                        diff += 1;
                        if r2_idx_i >= sim.highest_point {
                            break;
                        }
                    }
                    if diff >= (r2_idx - r1_idx) {
                        height_per_cycle = r2_idx - r1_idx;
                        cycle_start_idx = r1_idx;
                        cycle_start_row = Some(sim.cave[cycle_start_idx]);
                        println!(
                            "Found height: {height_per_cycle} starting from idx {cycle_start_idx}"
                        );
                        found = true;
                        break;
                    }
                }
            }
            if found {
                break;
            }
        }
    }
    // Restart the simulation to find exactly which step the cycle repeats
    let mut sim = Simulation::new(pushes.clone());
    let cycle_start_row = cycle_start_row.unwrap();
    println!("{cycle_start_row:?}");
    while cycle_start_row != sim.cave[cycle_start_idx] {
        sim.step();
    }
    println!("now find how many steps to repeat");
    let mut steps = 0;
    while cycle_start_row != sim.cave[cycle_start_idx + height_per_cycle] {
        sim.step();
        steps += 1;
    }
    println!("Steps per cycle is {steps}");
    steps_per_cycle = steps;

    let mut skip_steps = 0;
    while sim.step + skip_steps < (1000000000000 - steps_per_cycle) {
        skip_steps += steps_per_cycle;
        total_height += height_per_cycle;
    }while sim.step + skip_steps < 1000000000000 {
        sim.step();
    }

    println!("Part2: {}", total_height + sim.highest_point + 1); // Don't forget + 1 :)

}
