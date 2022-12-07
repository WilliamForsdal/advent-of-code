
class Dir:
    def __init__(self, name: str):
        self.name = name
        self.parent: Dir = None
        self.dirs: list["Dir"] = []
        self.files:    list[tuple] = []

    def add_child(self, child: str):
        (type, name) = child.split(" ")
        if type == "dir":
            dir = Dir(name)
            dir.parent = self
            self.dirs.append(dir)
        else:
            self.files.append((int(type), name))
            
    def size(self) -> int:
        return sum([dir.size() for dir in self.dirs]) + sum([f[0] for f in self.files])

    def sum_small_dirs(self) -> int:
        sum = 0
        if self.size() < 100000:
            sum += self.size()

        for dir in self.dirs:
            sum += dir.sum_small_dirs()
        return sum

def part1(lines: list):
    root = Dir("/")

    current_dir = None

    line_idx = 0
    while 1:
        if line_idx >= len(lines):
            break
        l = lines[line_idx]
        line_idx += 1
        if l[0] == "$":
            cmd = l[2:4]

            if cmd == "ls":
                while line_idx < len(lines) and lines[line_idx][0] != "$":
                    current_dir.add_child(lines[line_idx])
                    line_idx += 1
                continue

            if cmd == "cd":
                # change dir
                dst = l.split(" ")[-1]
                if dst == "/":
                    current_dir = root
                elif dst == "..":
                    current_dir = current_dir.parent
                else:
                    current_dir = next(dir for dir in current_dir.dirs if dir.name == dst)

    print("part1:", root.sum_small_dirs())
    return root

def part2(root: "Dir"):
    
    def find_smallest_ok_dir(current_dir: "Dir") -> "Dir":
        smallest = None
        for dir in current_dir.dirs:
            if dir.size() >= min_delete_size:
                if smallest is None:
                    smallest = dir
                elif smallest.size() < dir.size():
                    smallest = dir

                smallest_in_this_dir = find_smallest_ok_dir(dir)
                if smallest_in_this_dir is None:
                    continue
                if smallest_in_this_dir.size() < smallest.size():
                    smallest = smallest_in_this_dir

        return smallest

    total_disk_space = 70000000
    required_space = 30000000
    current_space = total_disk_space - root.size()
    min_delete_size = required_space - current_space
    
    smallest_ok_dir = find_smallest_ok_dir(root)
    print (f"part2: {smallest_ok_dir.size()}")


lines = []

with open("inputs/day7", "r") as f:
    lines = [l.strip() for l in f.readlines()]


root = part1(lines)
part2(root)
