

class Monkey:
    def __init__(self, idx: 0, lines: list[str], worry_div: int = 3):
        self.idx: int = idx
        self.inspections: int = 0
        self.items: list[int] = [int(s.strip()) for s in (lines[0].split(":")[1]).strip().split(", ")]
        self.op = lines[1].split(" = ")[1].split(" ")
        self.divisible_by = int(lines[2].split(" ")[-1])
        self.truemonk = int(lines[3].split(" ")[-1])
        self.falsemonk = int(lines[4].split(" ")[-1])
        self.worry_div = worry_div

    def business(self, monkeys: list["Monkey"]):
        for item in self.items.copy():
            # inspect
            item = self.inspect(item)
            self.inspections += 1

            # relief
            item = item // self.worry_div # integer divide

            # test and throw
            if (item % self.divisible_by) == 0:
                # print(f"monkey {self.idx} threw {item} to monkey {self.truemonk}")
                monkeys[self.truemonk].items.append(item)
            else:
                # print(f"monkey {self.idx} threw {item} to monkey {self.falsemonk}")
                monkeys[self.falsemonk].items.append(item)
        self.items.clear()


    def inspect(self, item: int):
        left = 0
        right = 0
        if self.op[0] == "old":
            left = item
        else:
            left = int(self.op[0])
        
        if self.op[2] == "old":
            right = item
        else:
            right = int(self.op[2])
        
        if self.op[1] == "*":
            return left * right
        if self.op[1] == "+":
            return left + right
        


def part1(monkeys):
    
    for round in range(0,20):
        # print(round)

        for monkey in monkeys:
            monkey.business(monkeys)

    top2 = sorted([m.inspections for m in monkeys])[-2:]
    print("Part1:", top2[0] * top2[1])
        

def part2(monkeys):
    for round in range(0,10000):
        print(round)

        for monkey in monkeys:
            monkey.business(monkeys)

    top2 = sorted([m.inspections for m in monkeys])[-2:]
    print("Part2:", top2[0] * top2[1])
        
lines = []
with open("inputs/day11") as f:
    lines = [l.strip() for l in f.readlines()]

monkeys = []

lines = lines[1:] # skip first monkey index

idx = 0
for n in range(0, len(lines), 7):
    monk = lines[:5]
    monkeys.append(Monkey(idx, monk))
    lines = lines[7:]
    idx += 1


part1(monkeys)

monkeys = []


with open("inputs/day11") as f:
    lines = [l.strip() for l in f.readlines()]

lines = lines[1:] # skip first monkey index

idx = 0
for n in range(0, len(lines), 7):
    monk = lines[:5]
    monkeys.append(Monkey(idx, monk, worry_div=1))
    lines = lines[7:]
    idx += 1


# part1(monkeys)