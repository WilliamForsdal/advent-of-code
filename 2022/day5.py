

def part1(buckets: list[list], moves):
    for move in moves:
        move = move[5:]
        l,r = move.split("from")
        l,r = (l.strip(), r.strip())
        r, r2 = r.split(" to ")
        amount = int(l)
        src = buckets[int(r) - 1]
        dst = buckets[int(r2) - 1]
        
        while amount:
            amount -= 1
            dst.append(src.pop())
    bees = ""
    for b in buckets:
        bees += b[-1]
    print ("part1:", bees)

def part2(buckets: list[list], moves):
    for move in moves:
        move = move[5:]
        l,r = move.split("from")
        l,r = (l.strip(), r.strip())
        r, r2 = r.split(" to ")
        amount = int(l)
        src_idx = int(r) - 1
        dst_idx = int(r2) - 1
        src = buckets[src_idx]
        for item in src[-amount:]:
            buckets[dst_idx].append(item)

        buckets[src_idx] = src[:-amount]


    bees = ""
    for b in buckets:
        bees += b[-1]
    print ("part2:", bees)


lines = []
with open("inputs/day5", "r") as f:
    lines = [l.strip() for l in f.readlines()]

columns = lines[:8]
moves = lines[10:]

buckets = [[], [], [], [], [], [], [], [], []]
for idx in range(0, 9):
    col = idx*4 + 1
    for l in columns:
        if l[col] == ' ':
            continue
        buckets[idx].insert(0, l[col])



part1(buckets, moves)

buckets = [[], [], [], [], [], [], [], [], []]
for idx in range(0, 9):
    col = idx*4 + 1
    for l in columns:
        if l[col] == ' ':
            continue
        buckets[idx].insert(0, l[col])

part2(buckets, moves)
