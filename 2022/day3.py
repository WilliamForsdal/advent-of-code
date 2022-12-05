
def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def prio(item_type):
    lower = item_type.lower()
    prio = ord(lower) - 96
    if item_type != lower:
        prio += 26
    return prio

def part1():
    
    with open("inputs/day3", "r") as f:
        sum = 0
        for line in f.readlines():
            line = line.strip()
            half = int(len(line) / 2)
            comp1, comp2 = (line[:half], line[half:])
            # print(comp1, comp2)
            common = list(set(comp1) & set(comp2))[0]
            sum += prio(common)
                
        print (sum)


def part2():
    with open("inputs/day3", "r") as f:
        sum = 0
        for lines in chunks(f.readlines(),3):
            lines = [l.strip() for l in lines]
            common = list(set(lines[0]) & set(lines[1]) & set(lines[2]))[0]
            sum += prio(common)
            # print(common, sum)


part1()
# part2()

