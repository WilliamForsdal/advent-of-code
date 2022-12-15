

class Sensor:
    def __init__(self, sx, sy, bx, by):
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

    print("part1:", result)


def part2(sensors: list["Sensor"]):
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

    # print(sum([(s.range+1)*4 for s in sensors]))

    sensor_number = 0
    for sensor in sensors:
        sensor_number += 1
        # print("Doing sensor", sensor_number, "of", len(sensors))
        print("Sensor", sensor_number, "of", len(sensors))
        left = (sensor.x - (sensor.range+1), sensor.y)
        x, y = left
        points = []
        for i in range(0, sensor.range + 1):
            if (x+i > beacon_max or x+i < 0 or y+i > beacon_max or y+i < 0 or y-i < 0):
                continue

            points.append((x + i, y - i))         # walk up-right
            points.append((x + i, y + i))         # walk down-right

        right = (sensor.x + (sensor.range+1), sensor.y)
        x, y = right
        for i in range(0, sensor.range + 1):
            if (x-i < 0 or x+i < 0 or y+i > beacon_max or y+i < 0 or y-i < 0):
                continue

            points.append((x - i, y - i))         # walk up-left
            points.append((x - i, y + i))         # walk down-left

        for p in points:
            if not in_range(p, sensors):
                print("part2:", p, " was the point, which gives:",
                      p[0]*4000000 + p[1])
                return


def in_range(point, sensors: list["Sensor"]) -> bool:
    if point[0] < 0 or point[0] > 4000000 or point[1] < 0 or point[1] > 4000000:
        return False
    for sensor in sensors:
        distance = (abs(point[0] - sensor.x) + abs(point[1] - sensor.y))
        if distance <= sensor.range:
            return True
    return False


input_lines = open("inputs/day15").read().strip().splitlines()
sensors = []

for l in input_lines:
    s, b = l.split(": ")
    sx, sy = s[10:].split(", ")
    sx, sy = (int(sx.split("=")[1]), int(sy.split("=")[1]))
    bx, by = b[21:].split(", ")
    bx, by = (int(bx.split("=")[1]), int(by.split("=")[1]))
    sensors.append(Sensor(sx, sy, bx, by))

part1(sensors)
part2(sensors)
