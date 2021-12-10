import sys

lines = sys.stdin.readlines()

openb = set('(<{[')
closeb = set(')>}]')

closemap = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>',
}

costmap = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

costmap2 = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}

def find_illegal(line):
    stack = []
    for c in line:
        if c in openb:
            stack.append(c)
        elif c in closeb:
            t = closemap[stack.pop()]
            if t != c:
                return c
        else:
            raise Exception(f"Invalid Char found: {c}")

cost = 0
for line in lines:
    line = line.strip()
    if line:
        illegal = find_illegal(line)
        if illegal:
            cost += costmap[illegal]
print(cost)

def complete_line(line):
    stack = []
    for c in line:
        if c in openb:
            stack.append(c)
        elif c in closeb:
            t = closemap[stack.pop()]
            if t != c:
                return None
        else:
            raise Exception(f"Invalid Char found: {c}")
    return [closemap[i] for i in stack[::-1]]

scores = []
for line in lines:
    line = line.strip()
    if line:
        complete = complete_line(line)
        if complete:
            cost = 0
            for c in complete:
                cost *= 5
                cost += costmap2[c]
            scores.append(cost)
print(sorted(scores)[len(scores) // 2])