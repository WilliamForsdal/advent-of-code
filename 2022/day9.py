LEFT = 'L'
RIGHT = 'R'
UP = 'U'
DOWN = 'D'


class P:
    def __init__(self):
        self.row = 0
        self.col = 0
    
    def follow(self, head: "P", moved):
        diff_col = head.col - self.col
        diff_row = head.row - self.row

        if moved == LEFT:
            if diff_col == -2:
                self.col -= 1
                if diff_row != 0:
                    self.row += diff_row
        if moved == RIGHT:
            if diff_col == 2:
                self.col += 1
                if diff_row != 0:
                    self.row += diff_row
        if moved == UP:
            if diff_row == -2:
                self.row -= 1
                if diff_col != 0:
                    self.col += diff_col
        if moved == DOWN:
            if diff_row == 2:
                self.row += 1
                if diff_col != 0:
                    self.col += diff_col



class Move:
    def __init__(self, dir, times):
        self.dir = dir
        self.times = times


def part1(moves):
    head = P()
    tail = P()

    tail_positions = [(0,0)] # starts at 0,0

    for move in moves:
        for _ in range(0, move.times):
            if move.dir == LEFT:
                head.col -= 1
            elif move.dir == RIGHT:
                head.col += 1
            elif move.dir == UP:
                head.row -= 1
            elif move.dir == DOWN:
                head.row += 1

            tail.follow(head, move.dir)
            tail_positions.append((tail.col, tail.row))
            # print(f"after move {move.dir} head is at {(head.row, head.col)} and tail is at {(tail.row, tail.col)}.")

    tail_positions = set(tail_positions)
    print("Part1:", len(tail_positions))
    # 6828 too high


def part2(moves):
    knots = [P(),P(),P(),P(),P(),P(),P(),P(),P(),P()]
    head = knots[0]
    tail = knots[-1]
    tail_positions = [(0,0)] # starts at 0,0
    
    for move in moves:
        for _ in range(0, move.times):
            if move.dir == LEFT:
                head.col -= 1
            elif move.dir == RIGHT:
                head.col += 1
            elif move.dir == UP:
                head.row -= 1
            elif move.dir == DOWN:
                head.row += 1

            prev_knot = head
            for knot in knots[1:]:
                knot.follow(prev_knot, move.dir)
                prev_knot = knot
            
            tail_positions.append((tail.col, tail.row))

    
    tail_positions = set(tail_positions)
    print("Part2:", len(tail_positions))
    

lines = []
with open("inputs/day9", "r") as f:
    lines = [l.strip() for l in f.readlines()]

moves = []
for l in lines:
    split = l.split(" ")
    moves.append(Move(split[0], int(split[1])))

part1(moves)
part2(moves)
