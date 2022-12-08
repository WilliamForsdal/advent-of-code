
def part1(text):
    idx = 0
    while True:
        if len(set(text[idx:idx+4])) == 4:
            print(f"Part1: {idx+4}")
            break
        idx += 1

def part2(text):
    idx = 0
    while True:
        if len(set(text[idx:idx+14])) == 14:
            print(f"Part2: {idx+14}")
            break
        idx += 1

s = ""
with open("inputs/day6") as f:
    s = f.readline()

part1(s)
part2(s)
