import os


def part1(grid, start):
    resting = 0
    draw_path = False
    while 1:
        row, col = start
        while 1:
            if row+1 >= len(grid):
                print("part1:", resting)
                return resting

            if grid[row+1][col] == ".":  # not occupied space below
                row += 1
                continue

            if grid[row+1][col-1] == ".":  # not occupied space below left
                row += 1
                col -= 1
                continue

            if grid[row+1][col+1] == ".":  # right
                row += 1
                col += 1
                continue

            # no space to move, make new sand
            resting += 1
            grid[row][col] = "O"
            break


def part2(grid, start, resting):
    while 1:
        row, col = start
        while 1:

            if grid[row+1][col] == ".":  # not occupied space below
                row += 1
                continue

            if grid[row+1][col-1] == ".":  # not occupied space below left
                row += 1
                col -= 1
                continue

            if grid[row+1][col+1] == ".":  # right
                row += 1
                col += 1
                continue

            # no space to move, make new sand

            resting += 1
            grid[row][col] = "O"

            if (row, col) == start:
                for l in grid:
                    print("".join(l[400:600]))
                print("part2:", resting)  # 29584 too high.
                return
            break


txt_lines = [l.strip()
             for l in open("inputs/day14").read().strip().splitlines()]


grid_lines = []

for l in txt_lines:
    coords = [s.strip() for s in l.split(" -> ")]

    col1, row1 = coords[0].split(",")

    for coord in coords[1:]:
        col2, row2 = coord.split(",")
        grid_lines.append((int(col1), int(row1), int(col2), int(row2)))
        col1, row1 = (col2, row2)

min_col = min([a[0] for a in grid_lines] + [a[2] for a in grid_lines])
max_col = max([a[0] for a in grid_lines] + [a[2] for a in grid_lines])
min_row = min([a[1] for a in grid_lines] + [a[3] for a in grid_lines])
max_row = max([a[1] for a in grid_lines] + [a[3] for a in grid_lines])

min_col = 0
max_col += 100

grid = []
for row in range(0, max_row+3):  # add an extra row below all
    r = []
    for col in range(min_col, max_col + 2):
        r.append('.')
    grid.append(r)

for line in grid_lines:
    col1, row1, col2, row2 = line

    # Must be horizontal or vertical line?
    if col1 != col2 and row1 != row2:
        raise Exception()

    while col1 != col2:
        grid[row1][col1-min_col] = "#"
        if col1 < col2:
            col1 += 1
        else:
            col1 -= 1
        grid[row1][col1-min_col] = "#"

    while row1 != row2:
        grid[row1][col1-min_col] = "#"
        if row1 < row2:
            row1 += 1
        else:
            row1 -= 1
        grid[row1][col1-min_col] = "#"

resting = part1(grid, (0, 500-min_col))

for (i, _) in enumerate(grid[-1]):
    grid[-1][i] = "#"

try:
    part2(grid, (0, 500-min_col), resting)
except:
    print ("ERROR")
