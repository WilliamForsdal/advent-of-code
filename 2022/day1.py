
def main():
    with open("inputs/day1", mode="r") as f:
        elves = []
        calories = 0
        for line in f.readlines():
            line = line.strip()
            if line == "":
                elves.append(calories)
                calories = 0
            else:
                calories += int(line)

        print("part1:", max(elves))
        print("part2:",sum(sorted(elves, reverse=True)[:3]))

main()