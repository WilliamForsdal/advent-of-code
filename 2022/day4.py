

def make_range(r) -> range:
    start,end = r.split("-")
    return range(int(start), int(end))


def part1(lines: list[str]):
    num_overlaps = 0
    for l in lines:
        a,b = l.split(",")
        a = make_range(a)
        b = make_range(b)
        if a.start >= b.start and a.stop <= b.stop:
            num_overlaps += 1
        elif b.start >= a.start and b.stop <= a.stop:
            num_overlaps += 1
    print("part1: ", num_overlaps)

def part2(lines: list[str]):
    num_overlaps = 0
    for l in lines:
        a,b = l.split(",")
        a = make_range(a)
        b = make_range(b)
        if a.start >= b.start and a.start <= b.stop:
            num_overlaps += 1
        elif b.start >= a.start and b.start <= a.stop:
            num_overlaps += 1

    print("part2: ", num_overlaps)




lines = []
with open("inputs/day4") as f:
    lines = [l.strip() for l in f.readlines()]

part1(lines)
part2(lines)

# 1000 too high
# 679 too low