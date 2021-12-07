import sys, math
from itertools import combinations
lines = sys.stdin.readlines()
points = [int(i) for i in lines[0].split(',')]

median = sorted(points)[len(points) // 2]
print(sum([abs(p - median) for p in points]))

mean = sum(points) / len(points)
lower = math.floor(mean)
higher = math.ceil(mean)
cost = lambda p: sum([sum(range(1, abs(p - i) + 1)) for i in points])
print(min([cost(lower), cost(higher)]))