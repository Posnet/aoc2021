import sys
from collections import Counter

def code_to_number(code):
    numbers = {
        0: set('abcefg'),
        1: set('cf'),
        2: set('acdeg'),
        3: set('acdfg'),
        4: set('bcdf'),
        5: set('abdfg'),
        6: set('abdefg'),
        7: set('acf'),
        8: set('abcdefg'),
        9: set('abcdfg'),
    }
    lookup = {''.join(sorted(''.join(v))): k for k,v in numbers.items()}
    return lookup[code]

def solve(numbers):
    nn = {}
    for v in numbers:
        v2 = nn.get(len(v), [])
        v2.append(v)
        nn[len(v)] = v2
    a = nn[3][0] - nn[2][0]

    cf = nn[2][0] - a

    known = a

    nn = {}
    for v in numbers:
        v = v - known
        v = v - cf
        v2 = nn.get(len(v), [])
        v2.append(v)
        nn[len(v)] = v2

    d = nn[2][0] & nn[2][1]

    known = a | d

    nn = {}
    for v in numbers:
        v = v - known
        v = v - cf
        v2 = nn.get(len(v), [])
        v2.append(v)
        nn[len(v)] = v2
    nn
    g = nn[2][0] & nn[2][1] & nn[2][2]

    known = a | d | g

    nn = {}
    for v in numbers:
        v = v - known
        v = v - cf
        v2 = nn.get(len(v), [])
        v2.append(v)
        nn[len(v)] = v2

    ctr = {}
    for v in nn[1]:
        v = v.pop()
        v2 = ctr.get(v, 0)
        v2 += 1
        ctr[v] = v2
    ctr = {v:k for k,v in ctr.items()}
    b = {ctr[3]}
    e = {ctr[1]}

    known = a | b | d | e | g

    nn = {}
    for v in numbers:
        v = v - known
        v2 = nn.get(len(v), [])
        v2.append(v)
        nn[len(v)] = v2
    nn

    ctr = {}
    for v in nn[1]:
        v = v.pop()
        v2 = ctr.get(v, 0)
        v2 += 1
        ctr[v] = v2
    ctr = {v:k for k,v in ctr.items()}
    c = {ctr[1]}
    f = {ctr[2]}

    lookup = {
        a.pop(): 'a',
        b.pop(): 'b',
        c.pop(): 'c',
        d.pop(): 'd',
        e.pop(): 'e',
        f.pop(): 'f',
        g.pop(): 'g'
    }
    return lookup


lines = sys.stdin.readlines()
broken = []
broken2 = []
for line in lines:
    key, numbers = line.split('|')
    keys = [set(v.strip()) for v in key.split()]
    codes = [v.strip() for v in numbers.split()]
    lookup = solve(keys)
    codes = [''.join(sorted([lookup[c] for c in co])) for co in codes]
    codes = [code_to_number(co) for co in codes]
    broken += codes
    broken2.append(codes[0] * 1000 + codes[1] * 100 + codes[2] * 10 + codes[3])

c = Counter(broken)

print(c[1] + c[4] + c[7] + c[8])

print(sum(broken2))
