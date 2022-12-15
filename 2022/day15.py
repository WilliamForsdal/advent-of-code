









class Sensor:
    def __init__(self, sx,sy,bx,by):
        self.x = sx
        self.y = sy

        self.beacon_x = bx
        self.beacon_y = by

        self.range = abs(sx - bx) + abs(sy - by)


def part1(sensors: list):
    ranges = []
    row = 2000000
    for s in sensors:
        x = s.x
        diff_y = abs(s.y - row)
        range = (s.range - diff_y)
        if range <= 0:
            continue
        lower = s.x - range
        upper = s.x + range
        ranges.append((lower, upper))

    ranges = sorted(ranges)

    result = []
    idx = 0
    while 1:
        if idx >= len(ranges):
            break

        new_range = (ranges(idx)[0],ranges(idx)[1])
        for i,r2 in enumerate(ranges[idx:]):
            if new_range[1] >= r2[0]:
                new_range = (new_range[0], new_range[1])
                idx = i

















input_lines = open("inputs/day15").read().strip().splitlines()
sensors = []

for l in input_lines:
    s,b = l.split(": ")
    sx,sy = s[10:].split(", ")
    sx,sy = (int(sx.split("=")[1]), int(sy.split("=")[1]))
    bx,by = b[21:].split(", ")
    bx,by = (int(bx.split("=")[1]), int(by.split("=")[1]))
    sensors.append(Sensor(sx,sy,bx,by))

part1(sensors)