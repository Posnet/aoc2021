import sys

lines = list(sys.stdin.readlines())
lines = [tuple(line.strip().split(" ")) for line in lines]
agg = {
    "forward": 0,
    "up": 0,
    "down": 0,
}

for kind, size in lines:
    agg[kind] += int(size)
print((agg["down"] - agg["up"]) * agg["forward"])

forward = 0
aim = 0
depth = 0
for kind, size in lines:
    size = int(size)
    if kind == "up":
        aim -= size
    if kind == "down":
        aim += size
    if kind == "forward":
        forward += size
        depth += size * aim
print(forward * depth)
