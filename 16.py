import sys
from pprint import pprint

def hex2bin(hex):
    lookup = {
        "0": "0000",
        "1": "0001",
        "2": "0010",
        "3": "0011",
        "4": "0100",
        "5": "0101",
        "6": "0110",
        "7": "0111",
        "8": "1000",
        "9": "1001",
        "A": "1010",
        "B": "1011",
        "C": "1100",
        "D": "1101",
        "E": "1110",
        "F": "1111", 
    }
    res = ''
    for c in hex:
        res += lookup[c]

    return res

lines = sys.stdin.read().splitlines()
lines = [hex2bin(l) for l in lines]


def ppacket(data, limit=None):
    version_sum = 0
    packets = []
    while len(data) > 6 and set(data) != {'0'}:
        version = int(data[:3], 2)
        version_sum += version
        kind = int(data[3:6], 2)
        data = data[6:]
        if kind == 4:  # literal
            number = ''
            while len(data) >= 5:
                terminal = int(data[0])
                number += data[1:5]
                data = data[5:]
                if terminal == 0:
                    break
            packets.append((version, kind, int(number, 2)))
        else:
            lt = int(data[0])
            data = data[1:]
            if lt:
                pcount = int(data[:11], 2)
                data = data[11:]
                sub_packets, data, vs = ppacket(data, limit=pcount)
            else:
                plen = int(data[:15], 2)
                data = data[15:]
                sub_data = data[:plen]
                data = data[plen:]
                sub_packets, _, vs = ppacket(sub_data)
            packets.append((version, kind, sub_packets))
            version_sum += vs
        if limit and len(packets) >= limit:
            break
    return packets, data, version_sum


def evaluate(packets):
    result = []
    for version, kind, content in packets:
        if kind == 4:
            result.append(content)
        else:
            values = evaluate(content)
            if kind == 0:
                result.append(sum(values))
            elif kind == 1:
                res = 1
                for v in values:
                    res *= v
                result.append(res)
            elif kind == 2:
                result.append(min(values))
            elif kind == 3:
                result.append(max(values))
            elif kind == 5:
                left, right = values
                result.append(int(left > right))
            elif kind == 6:
                left, right = values
                result.append(int(left < right))
            elif kind == 7:
                left, right = values
                result.append(int(left == right))
    return result

for line in lines:
    line = line.strip()
    if line:
        packets, rem, vs = ppacket(line)
        print("eval:", evaluate(packets)[0])
        print()