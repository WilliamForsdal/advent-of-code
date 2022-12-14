import sys


class Grid:
    def __init__(self, raw_grid: list[list[int]]):
        self.width = len(raw_grid[0])
        self.height = len(raw_grid)
        self.raw_grid = raw_grid
        self.nodes: list[list["Node"]] = []

        r = 0
        for row in raw_grid:
            c = 0
            nodes_row = []
            for col in row:
                nodes_row.append(Node(self, r, c, col))
                c += 1
            self.nodes.append(nodes_row)
            r += 1

    def all_nodes(self):
        for r in self.nodes:
            for c in r:
                yield c

    def print(self):

        with open("grid.txt", "w") as f:
            for row in self.nodes:
                f.write(" ".join(
                    [(f"{n.distance:3}" if n.distance < 999 else f' # ') for n in row]))
                f.write("\n")
        print("Saved grid.txt")


class Node:
    def __init__(self, grid: "Grid", row: int, col: int, height: int):
        self.grid: "Grid" = grid
        self.row: int = row
        self.col: int = col
        self.height: int = height
        self.distance = 99999  # not calculated
        self.visited = False

    def neighbors(self):
        return [n for n in [self.right, self.up, self.down, self.left] if n is not None]

    @property
    def up(self):
        if self.row == 0:
            return None
        node = self.grid.nodes[self.row-1][self.col]
        if node.height - self.height > 1:
            return None
        return node

    @property
    def down(self):
        if self.row+1 >= self.grid.height:
            return None
        node = self.grid.nodes[self.row+1][self.col]
        if node.height - self.height > 1:
            return None
        return node

    @property
    def left(self):
        if self.col == 0:
            return None
        node = self.grid.nodes[self.row][self.col-1]
        if node.height - self.height > 1:
            return None
        return node

    @property
    def right(self):
        if self.col + 1 >= self.grid.width:
            return None
        node = self.grid.nodes[self.row][self.col + 1]
        if node.height - self.height > 1:
            return None
        return node

    def update_neighbors(self, path: list["Node"], max: int = 500):
        if len(path) > max:
            return
        if self in path:
            return
        self.visited = True
        path.append(self)
        for n in self.neighbors():
            if n.distance > self.distance + 1:
                n.distance = self.distance + 1
                n.update_neighbors(path)
        if path.pop() != self:
            raise Exception()


def part1(raw_grid, start, end):
    grid = Grid(raw_grid)
    start = grid.nodes[start[0]][start[1]]
    end = grid.nodes[end[0]][end[1]]
    start.distance = 0
    path = []
    start.update_neighbors(path)
    print("part1:", end.distance)


def part2(raw_grid, end):
    minimum = 482
    # Searching all 'a's takes a minute or two.
    # for start_row in range(0, len(raw_grid)):
    for _ in range(0,1): # to
        # print ("checking", start_row+1, "of", len(raw_grid))
        grid = Grid(raw_grid)
        start = grid.nodes[19][0]
        start.distance = 0
        start.update_neighbors([], minimum)
        end_node = grid.nodes[end[0]][end[1]]
        # print("distance:", end_node.distance)
        if end_node.distance < minimum:
            minimum = end_node.distance

    print("Part2:", minimum)


lines = []
with open("inputs/day12") as f:
    lines = [l.strip() for l in f.readlines()]

start = (0, 0)
end = (0, 0)
raw_grid = []
row = 0
for l in lines:
    r = []
    col = 0
    for c in l:
        if c == "S":
            r.append(ord("a"))
            start = (row, col)
        elif c == "E":
            r.append(ord("z"))
            end = (row, col)
        else:
            r.append(ord(c))
        col += 1
    row += 1

    raw_grid.append(r)

part1(raw_grid, start, end)
part2(raw_grid, end)
