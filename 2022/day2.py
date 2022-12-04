
ROCK = 0
PAPER = 1
SCISSORS = 2

def move_from_outcome(elf, outcome):
    if outcome == "X":
        return (elf + 2) % 3

    if outcome == "Y":
        return elf

    if outcome == "Z":
        return (elf + 1) % 3

def what(value):
    if value == "A":
        return ROCK
    if value == "B":
        return PAPER
    if value == "C":
        return SCISSORS
    
def main():
    with open("inputs/day2", mode="r") as file:
        my_points = 0
        for line in file.readlines():
            line = line.strip()
            elf, outcome = (what(line[0]), line[2])
            me = move_from_outcome(elf, outcome)
            my_points = my_points + points(elf, me)
        print("part2:", my_points)

def points(elf, me):
    result = me + 1 
    if elf == me: # This is a tie!
        result += 3
    if( (elf + 1)%3 == me):
        result += 6
    return result


main()