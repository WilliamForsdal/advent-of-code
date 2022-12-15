
import ast
from functools import cmp_to_key

def parse_list(pkt) -> list:
    return ast.literal_eval(pkt)


def part1(packet_pairs):
    pair_idx = 1
    pair_sum = 0
    for pair in packet_pairs:
        pkt1 = parse_list(pair[0])
        pkt2 = parse_list(pair[1])
        
        if do_compare(pkt1, pkt2) <= 0:
            pair_sum += pair_idx

        pair_idx += 1

    print("part1:", pair_sum)


def part2(packets):
    packets = [parse_list(packet) for packet in packets if len(packet) > 0]
    packets.append([[2]])
    packets.append([[6]])
    packets = sorted(packets, key=cmp_to_key(do_compare))
    res = (packets.index([[2]]) + 1) * (packets.index([[6]]) + 1) # +1 for 1based index....
    print("part2:", res)

def do_compare(pkt1, pkt2) -> int:
    if isinstance(pkt1, int) and isinstance(pkt2, int):
        if pkt1 == pkt2:
            return 0
        elif pkt1 < pkt2:
            return -1
        else:
            return 1

    elif isinstance(pkt1, list) and isinstance(pkt2, list):
        min_len = min(len(pkt1), len(pkt2))
        for idx in range(0, min_len):
            res = do_compare(pkt1[idx], pkt2[idx])
            if res == 0:
                continue
            elif res == 1:
                return 1
            else:
                return -1
            
        return do_compare(len(pkt1), len(pkt2))
        
    elif isinstance(pkt1, int) and isinstance(pkt2, list):
        return do_compare([pkt1], pkt2)
    elif isinstance(pkt1, list) and isinstance(pkt2, int):
        return do_compare(pkt1, [pkt2])
    else:
        raise Exception()




inp = open("inputs/day13").read().strip().splitlines()


packet_pairs = []

for x in range(0, len(inp), 3):
    packet_pairs.append((inp[x], inp[x+1]))

part1(packet_pairs)

packets = []

for x in range(0, len(inp), 3):
    packets.append(inp[x])
    packets.append(inp[x+1])

part2(packets)