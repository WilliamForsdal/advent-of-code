









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
        ydiff = (s.range - diff_y)
        if ydiff <= 0:
            continue
        lower = s.x - ydiff
        upper = s.x + ydiff
        ranges.append((lower, upper))

    ranges = sorted(ranges)
    minimum = min([r[0] for r in ranges])
    maximum = max([r[1] for r in ranges])

    result = 0
    for x in range(minimum, maximum):
        for r in ranges:
            if x >= r[0] and x <= r[1]:
                result += 1
                break

    print ("part1:", result)




def part2(sensors: list):
    beacon_max = 4000000
    
    ranges = []
    row = 10
    for s in sensors:
        x = s.x
        diff_y = abs(s.y - row)
        ydiff = (s.range - diff_y)
        if ydiff <= 0:
            continue
        lower = s.x - ydiff
        upper = s.x + ydiff
        ranges.append((lower, upper))

    ranges = sorted(ranges)
    minimum = min([r[0] for r in ranges])
    maximum = max([r[1] for r in ranges])

    points = []
    print(sum([(s.range+1)*4 for s in sensors]))
    for i in range(0, 79006864):
        # points.append("a")
        if i % 1000000 == 0:
            print(i)
    for sensor in sensors:
        pass
        # num_edges = (sensor.range + 1) * 4
        





























input_lines = open("inputs/day15").read().strip().splitlines()
sensors = []

for l in input_lines:
    s,b = l.split(": ")
    sx,sy = s[10:].split(", ")
    sx,sy = (int(sx.split("=")[1]), int(sy.split("=")[1]))
    bx,by = b[21:].split(", ")
    bx,by = (int(bx.split("=")[1]), int(by.split("=")[1]))
    sensors.append(Sensor(sx,sy,bx,by))

# part1(sensors)
part2(sensors)