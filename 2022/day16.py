import itertools
import functools

class Valve:
    def __init__(self, name, rate):
        self.name = name
        self.rate = rate
        self.tunnels_txt = []
        self.tunnels = []
        pass

    def shortest_path_to(self, other, path: list) -> list:
        if self in path:
            return None
        if len(path) > 30:
            return None

        path.append(self)

        if self == other:
            return path

        shortest = None
        for tunnel in self.tunnels:
            l = tunnel.shortest_path_to(other, path.copy())
            if l is None:
                continue
            if shortest is None or len(l) < len(shortest):
                shortest = l

        return shortest

    def __repr__(self):
        return self.name + f" ({self.rate})"


def part1(valves: list[Valve], shortest_paths: list[list[Valve]]):
    start = next(v for v in valves if v.name == "AA")

    openable = sorted([v for v in valves if v.rate > 0],
                      key=lambda x: x.rate, reverse=True)
    unopened = openable.copy()
    best = search(start, unopened, 30, shortest_paths)
    print(f"Part1:  {best}")
    

def part2(valves: list[Valve], shortest_paths: list[list[Valve]]):
    start = next(v for v in valves if v.name == "AA")

    openable = sorted([v for v in valves if v.rate > 0],
                      key=lambda x: x.rate, reverse=True)
    unopened = openable.copy()
    print("Calculating best routes.")
    # for num_elephant_valves in range(1, len(valves)//2):
    #     print(f"At {num_elephant_valves}... {count}")
    
    import multiprocessing as mp
    num_cpus = mp.cpu_count()

    pool = mp.Pool(num_cpus)

    all = list(itertools.combinations(openable, 8))

    def elephant_search(elephant_valves_lst):
        best = 0
        for elephant_valves in elephant_valves_lst:
            my_valves = [v for v in valves if v not in elephant_valves]
            elephant_score = search(start, list(elephant_valves), 26, shortest_paths)
            my_score = search(start, my_valves, 26, shortest_paths)
            if best < elephant_score + my_score:
                best = elephant_score + my_score
                print("Found new best:", best)

    results = [pool.apply(elephant_search, args=e) for e in [all[i:i+num_cpus] for i in range(0, len(all), num_cpus)]]
        
    print(f"Part2:  {max(results)}")
    # 1921 too low
    # 2102 too high

@functools.cache
def search(current: Valve, unopened: list[Valve], time_left: int, shortest_paths: list[list[Valve]]) -> int:
    unopened = unopened.copy()
    if current in unopened:
        unopened.remove(current)
    best = 0
    for v in unopened:
        # if current.name == "AA":
        #     print(f"Checking from {current} to {v}")

        for path in [p for p in shortest_paths if p[0] == current and p[-1] == v]:
            # -1 because we don't count the first element, and + 1 to open the valve.
            time = len(path)
            # Equals because it's only worth anything if it actually has time to psssssh out steam
            if (time_left - time) <= 0:
                continue

            # If we walk down this path, we release this valve and the best from this valve.
            release = (time_left - time) * v.rate
            release += search(path[-1], unopened,
                              time_left - time, shortest_paths)
            if release > best:
                best = release
                # print(f"New best: from {current} to {v} is {best}")

    return best


# Define a cost function for steps
def cost(unopened: list[Valve]):
    return sum([v.rate for v in unopened])


lines = open("inputs/day16").read().strip().splitlines()

valves: list[Valve] = []
# Valve AA has flow rate=0; tunnels lead to valves KH, EJ, OM, TY, DO
for l in lines:
    b, f = l.split(";")
    name = b[6:8]
    rate = int(b.split("=")[1])
    # print(f"{name}, {rate}")
    valve = Valve(name, rate)
    valves.append(valve)

    for tunnel in f.strip()[22:].split(","):
        valve.tunnels_txt.append(tunnel.strip())

for valve in valves:
    for tunnel in valve.tunnels_txt:
        leads_to = next(v for v in valves if v.name == tunnel)
        valve.tunnels.append(leads_to)


start = next(v for v in valves if v.name == "AA")
openable = sorted([v for v in valves if v.rate > 0], key=lambda x: x.rate, reverse=True)
unopened = openable.copy()
shortest_paths: list[list[Valve]] = []
print("Calculating shortest paths...")
for valve1 in (openable + [start]):
    for valve2 in openable:
        if valve1 == valve2:
            continue
        shortest = valve1.shortest_path_to(valve2, [])
        shortest_paths.append(shortest)

# part1(valves, shortest_paths)
part2(valves, shortest_paths)


# ZX, BV, HR, PD, FN
