import random


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
        if len(path) >= 30:
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


def part1(valves: list[Valve]):
    #
    start = next(v for v in valves if v.name == "AA")

    openable = sorted([v for v in valves if v.rate > 0],
                      key=lambda x: x.rate, reverse=True)
    # print(f"The {len(openable)} valves are:", [f"{v.name}:{v.rate}" for v in openable])

    shortest_paths: list[list[Valve]] = []
    print("Calculating shortest paths...")
    for valve1 in (openable + [start]):
        # print(valve1.name)
        for valve2 in openable:
            if valve1 == valve2:
                continue
            shortest = valve1.shortest_path_to(valve2, [])
            shortest_paths.append(shortest)

    from_aa = [p for p in shortest_paths if p[0] == start]
    from_bv = [p for p in shortest_paths if p[0].name == "BV"]

    for path in from_aa:
        print(path)

    t = 30
    max_score = sum([v.rate * t for v in openable]) 
    # Max score is 5940 if all valves are opened instantly. Too high of course.
    # 1132 is too low!

    opened = []
    current = start
    total_pressure_released = 0
    path_to_walk = []
    while t >= 0:
        best_pressure_release = 0
        best_path = None
        for path in [p for p in shortest_paths if p[0] == current and p[-1] not in opened]:
            time = len(path) # -1 because we don't count the first element, and + 1 to open the valve.
            if (t - time) <= 0:
                continue
            pressure = path[-1].rate * (t - time)
            if pressure > best_pressure_release:
                best_pressure_release = pressure
                best_path = path
        
        if best_path is None:
            print(t, best_pressure_release, pressure, path_to_walk)
            break    
        total_pressure_released += best_pressure_release
        t -= len(best_path)
        print(f"Walked {best_path} which released {best_pressure_release} pressure")
        current = best_path[-1]
        opened.append(current)
        path_to_walk += best_path
    
    print("part1:", total_pressure_released)

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


# print mermaid diagram
# for valve in valves:
#     for tunnel in valve.tunnels:
#         print(f"    {valve.name}_{valve.rate} --> {tunnel.name}_{tunnel.rate}")

part1(valves)


# ZX, BV, HR, PD, FN
