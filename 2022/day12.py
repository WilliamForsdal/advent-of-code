
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


class Node:
    def __init__(self, grid: "Grid", row: int, col: int, height: int):
        self.grid: "Grid" = grid
        self.row: int = row
        self.col: int = col
        self.height: int = height

    @property
    def up(self):
        if self.row == 0:
            return None
        return self.grid.nodes[self.row-1][self.col]

    @property
    def down(self):
        if self.row+1 >= self.grid.height:
            return None
        return self.grid.nodes[self.row+1][self.col]

    @property
    def left(self):
        if self.col == 0:
            return None
        return self.grid.nodes[self.row][self.col-1]

    @property
    def right(self):
        if self.col + 1 >= self.grid.width:
            return None
        return self.grid.nodes[self.row][self.col + 1]


def part1(grid: "Grid"):
    path: list["Node"] = []
    start = grid.nodes[20][0]
    end = grid.nodes[20][139]
    
    # if can't move towards 

    


lines = []
with open("inputs/day12") as f:
    lines = [l.strip() for l in f.readlines()]


raw_grid = []
for l in lines:
    row = []
    for c in l:
        row.append(ord(c))

    raw_grid.append(row)

grid = Grid(raw_grid)

part1(grid)
