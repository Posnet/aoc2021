import os
import sys
import time
from termcolor import colored
from random import shuffle
from collections import defaultdict
from sortedcontainers import SortedSet

lines = sys.stdin.readlines()

grid = []
global_id = 0

os.system('clear')

def move(y, x):
    print("\033[%d;%dH" % (y, x))

def print_grid(grid):
    data = []
    for y in range(h):
        for x in range(w):
            point = grid[y][x]
            data.append(str(point))
        data.append('\n')
    move(0, 0)
    # os.system('clear')
    print(' ', ' '.join(data))
    # time.sleep(0.2)


class Node:
    def __init__(self, cost):
        global global_id
        self.idx = global_id
        global_id += 1
        self.cost = cost
        self._edges = []
        self.visited = False
        self.path = False

    @property
    def edges(self):
        return self._edges

    def __le__(self, other):
        return self.cost <= other.cost

    def __lt__(self, other):
        return self.cost < other.cost

    def __eq__(self, other):
        return self.idx == other.idx

    def __hash__(self):
        return self.idx

    def reconstruct(self):
        pass

    def __repr__(self):
        if self.path:
            return colored(str(self.cost), "red")
        if self.visited:
            return colored(str(self.cost), "green")
        else:
            return str(self.cost)


def search(start, end, mcost, cb=None):
    cost = defaultdict(lambda: mcost)
    cost[start] = start.cost
    prev = {}
    visited = set()
    frontier = SortedSet(key=lambda x: -cost[x])
    frontier.add(start)
    ctr = 0
    while len(frontier) > 0:
        ctr += 1
        if ctr % 100 == 0 and cb:
            cb()
        n = frontier.pop()
        if n == end:
            path = []
            while True:
                p = prev[n]
                if p == start:
                    n.path = True
                    start.path = True
                    path.append(n)
                    path.append(start)
                    return path[::-1]
                else:
                    n.path = True
                    path.append(n)
                    n = p

        for e in n.edges:
            if cost[n] + e.cost < cost[e]:
                cost[e] = cost[n] + e.cost
                prev[e] = n
            if e not in visited:
                frontier.add(e)
        n.visited = True
        visited.add(n)
    return None



for line in lines:
    line = line.strip()
    if line:
        grid.append([int(i) for i in line])

w = len(grid[0])
h = len(grid)

nodes = []
ng = [[-1] * w * 5 for _ in range(h * 5)]
for y in range(len(ng[0])):
    for x in range(len(ng)):
        n = grid[x % w][y % h] + (x // w) + (y // h)
        if n > 9:
            n = (n % 10) + 1
        n = Node(n)
        nodes.append(n)
        ng[x][y] = n

grid = ng

w = len(grid[0])
h = len(grid)

adj = [(-1, 0), (+1, 0), (0, -1), (0, +1)]
total_cost = 0
for y in range(h):
    for x in range(w):
        node = grid[y][x]
        total_cost += node.cost
        for i, j in adj:
            xi = x + i
            yj = y + j
            if xi < 0 or xi >= w or yj < 0 or yj >= h:
                continue
            else:
                neb = grid[yj][xi]
                node._edges.append(neb)


path = search(nodes[0], nodes[-1], total_cost)
# print_grid(grid)
print(sum([c.cost for c in path[1:]]))
