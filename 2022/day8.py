



def part1(grid):
    width = len(grid)
    height = width # assume width == height

    visible_trees: list[tuple] = []
    
    # from left
    for x in range(0, height):
        highest = -1
        for y in range(0, width):
            if grid[x][y] > highest:
                visible_trees.append((x,y))
                highest = grid[x][y]

    # from above
    for x in range(0, height):
        highest = -1
        for y in range(0, width):
            if grid[y][x] > highest:
                visible_trees.append((y,x))
                highest = grid[y][x]
    
    # from right
    for x in reversed(range(0, height)):
        highest = -1
        for y in reversed(range(0, width)):
            if grid[x][y] > highest:
                visible_trees.append((x,y))
                highest = grid[x][y]
    

    # from below
    for x in reversed(range(0, height)):
        highest = -1
        for y in reversed(range(0, width)):
            if grid[y][x] > highest:
                visible_trees.append((y,x))
                highest = grid[y][x]


    visible_trees_set = set(visible_trees)
    print("part1:", len(visible_trees_set))
    return visible_trees_set

def part2(grid, visible_trees):
    grid_width = len(grid)
    grid_height = len(grid)

    def sightline_points(tree_col,tree_row):
        current_height = grid[tree_row][tree_col]
        
        col = tree_col
        row = tree_row
        # left
        sightline_left = 0
        while 1:
            col -= 1
            if col < 0:
                break
            sightline_left += 1
            h = grid[row][col]
            if h >= current_height:
                break

        # right
        col = tree_col
        row = tree_row
        sightline_right = 0
        while 1:
            col += 1
            if col >= grid_width:
                break
            sightline_right += 1
            h = grid[row][col]
            if h >= current_height:
                break

        # up
        col = tree_col
        row = tree_row
        sightline_up = 0
        while 1:
            row -= 1
            if row < 0:
                break

            sightline_up += 1
            h = grid[row][col]
            if h >= current_height:
                break

        # down
        col = tree_col
        row = tree_row
        sightline_down = 0
        while 1:
            row += 1
            if row >= grid_height:
                break

            sightline_down += 1
            h = grid[row][col]
            if h >= current_height:
                break

        return sightline_down * sightline_up * sightline_left * sightline_right

    highest_score = 0    
    for tree in visible_trees:
        score = sightline_points(tree[1], tree[0]) # accidentally used X as row, should be Y...
        if score > highest_score:
            highest_score = score

    print(f"Part2: {highest_score}")


lines = []
with open("inputs/day8", "r") as f:
    lines = [l.strip() for l in f.readlines()]


grid = []

for l in lines:
    row = []
    for c in l:
        row.append(int(c))
    grid.append(row)

visible_trees = part1(grid)
part2(grid, visible_trees)