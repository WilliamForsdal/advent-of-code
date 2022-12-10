
interesting_cycles = [20, 60, 100, 140, 180, 220]

class CPU:
    def __init__(self, instructions: list[str]):
        self.part1_result = 0
        
        self.instructions = [l.split(" ") for l in instructions]
        self.pc = 0
        self.cycle = 0
        self.x = 1
        self.executing_add = False
        self.display = ['.'] * 240

    def get_instruction(self):
        return self.instructions[self.pc] if self.pc < len(self.instructions) else None

    def tick(self):
        self.cycle += 1
        instr = self.get_instruction()
        if instr is None:
            return

        if instr[0] == "noop":
            self.mid_cycle()
            self.pc += 1

        elif instr[0] == "addx":
            if self.executing_add:
                self.executing_add = False
                self.mid_cycle()
                self.x += int(instr[1])
                self.pc += 1
            else:
                self.mid_cycle()
                self.executing_add = True

    def mid_cycle(self):
        if self.cycle in interesting_cycles:
            self.part1_result += (self.x * self.cycle)

        self.draw_pixel()

    def draw_pixel(self):
        x = self.x % 40
        c = (self.cycle-1) % 40
        if x == c or x-1 == c or x+1 == c:
            self.display[self.cycle] = '#'
        



def part1(lines):
    cpu = CPU(lines)
    for _ in range(0, 250):
        cpu.tick()

    print("part1:", cpu.part1_result)


def part2(lines):
    cpu = CPU(lines)
    for _ in range(0, 250):
        cpu.tick()
    
    print("part2:")
    for n in range(0, 240, 40):
        print("".join(cpu.display[n:n+40]))


lines = []
with open("inputs/day10", "r") as f:
    lines = [l.strip() for l in f.readlines()]



part1(lines)
part2(lines)
