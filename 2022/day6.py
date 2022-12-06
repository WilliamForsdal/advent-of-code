


def part1(stream):
    idx = 0
    while True:
        sett = set(stream[idx:idx+4])
        if len(sett) == 4:
            print(f"Part1: {idx+4}")
            break
        idx += 1


def part2(stream):
    idx = 0
    while True:
        sett = set(stream[idx:idx+14])
        if len(sett) == 14:
            print(f"Part2: {idx+14}")
            break
        idx += 1



string = ""
with open("inputs/day6") as f:
    string = f.readline()

part1(string)
part2(string)

