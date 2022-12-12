
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


class Node:
    def __init__(self, grid: "Grid", row: int, col: int, height: int):
        self.grid: "Grid" = grid
        self.row: int = row
        self.col: int = col
        self.height: int = height

    def neighbors(self):
        return [n for n in [self.up, self.right, self.down, self.left] if n is not None]

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

    def shortest_path_to(self, path: list["Node"], dest: "Node"):
        if self in path:
            return None
        path.append(self)
        print(self.height, self.row, self.col)
        if self.right == dest:
            return path + [self.right]
        if self.down == dest:
            return path + [self.down]
        if self.up == dest:
            return path + [self.up]
        if self.left == dest:
            return path + [self.left]

        right = None
        up = None
        down = None
        left = None

        if self.right is not None and self.right not in path:
            right = self.right.shortest_path_to(path.copy(), dest)
        if self.up is not None and self.up not in path:
            up = self.up.shortest_path_to(path.copy(), dest)
        if self.down is not None and self.down not in path:
            down = self.down.shortest_path_to(path.copy(), dest)
        if self.left is not None and self.left not in path:
            left = self.left.shortest_path_to(path.copy(), dest)

        paths = [p for p in [right, up, down, left] if p is not None]
        if len(paths) == 0:
            return None

        paths.sort(key=len)
        return paths[0]


def part1(grid: "Grid", start, end):
    deez = [n for n in grid.all_nodes() if n.height == ord("d")]

    # if can't move towards
    path = []
    shortest = start.shortest_path_to(path, end)
    print("part1:", len(shortest))


lines = []
with open("inputs/day12") as f:
    lines = [l.strip() for l in f.readlines()]

start = (0, 0)
end = (0, 0)
raw_grid = []
row = 0
for l in lines:
    row = []
    col = 0
    for c in l:
        if c == "S":
            row.append(ord("a"))
            start = (row, col)
        elif c == "E":
            row.append(ord("z"))
            end = (row, col)
        else:
            row.append(ord(c))
        col += 1
    row += 1

    raw_grid.append(row)

grid = Grid(raw_grid)

part1(grid, start, end)
