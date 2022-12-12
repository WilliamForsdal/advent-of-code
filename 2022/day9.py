LEFT = 'L'
RIGHT = 'R'
UP = 'U'
DOWN = 'D'


class P:
    def __init__(self, head: "P" = None):
        self.head = head
        self.row = 0
        self.col = 0

    def follow(self):
        head = self.head
        if head is None:
            # print(f"({self.row},{self.col})")
            return
            
        diff_col = head.col - self.col
        diff_row = head.row - self.row

        if abs(diff_col) == 2 and abs(diff_row) == 2:
            c = (1 if diff_col > 1 else -1)
            r = (1 if diff_row > 1 else -1)
            self.col += c
            self.row += r

        elif diff_col == -2:
            self.col -= 1
            if diff_row != 0:
                self.row += diff_row
        elif diff_col == 2:
            self.col += 1
            if diff_row != 0:
                self.row += diff_row
        elif diff_row == -2:
            self.row -= 1
            if diff_col != 0:
                self.col += diff_col
        elif diff_row == 2:
            self.row += 1
            if diff_col != 0:
                self.col += diff_col
        
        # print(f"({self.row},{self.col})")


class Move:
    def __init__(self, dir, times):
        self.dir = dir
        self.times = times


def print_board(size: int, knots: list[P]):
    origin = (size//2, size//2)
    grid = []
    for row in range(0, size):
        row = []
        for col in range(0, size):
            row.append(".")

        grid.append(row)
    knot_idx = 9
    for knot in reversed(knots):
        knot_name = ("H" if knot_idx == 0 else str(knot_idx))
        grid[knot.row + origin[0]][knot.col + origin[1]] = knot_name
        knot_idx -= 1


    for l in grid:
        
        print("".join(l))



def part1(moves):
    head = P()
    tail = P(head)

    tail_positions = [(0, 0)]  # starts at 0,0

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

            tail.follow()
            tail_positions.append((tail.col, tail.row))

    tail_positions = set(tail_positions)
    print("Part1:", len(tail_positions))

def part2(moves):
    head = P()
    knots = [head]
    for head_idx in range(0,9):
        knots.append(P(knots[head_idx]))

    head = knots[0]
    tail = knots[-1]
    tail_positions = [(0, 0)]  # starts at 0,0

    for move in moves:
        for _ in range(0, move.times):
            # print(f"move: {move.dir}")
            if move.dir == LEFT:
                head.col -= 1
            elif move.dir == RIGHT:
                head.col += 1
            elif move.dir == UP:
                head.row -= 1
            elif move.dir == DOWN:
                head.row += 1

            for knot in knots:
                knot.follow()


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

