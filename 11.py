import sys
import os
from termcolor import colored
lines = sys.stdin.readlines()

global_id = 0

os.system('clear')


def move(y, x):
    print("\033[%d;%dH" % (y, x))


def print_grid(grid):
    data = []
    w = len(grid[0])
    h = len(grid)
    for y in range(h):
        for x in range(w):
            point = grid[y][x]
            data.append(str(point))
        data.append('\n')
    # move(0, 0)
    os.system('clear')
    print(''.join(data))
    time.sleep(0.01)


class Node:
    def __init__(self, energy):
        global global_id
        self.idx = global_id
        global_id += 1
        self.energy = energy
        self._edges = []
        self.flashed = False

    @property
    def edges(self):
        return self._edges

    def __eq__(self, other):
        return self.idx == other.idx

    def __hash__(self):
        return self.idx

    def __repr__(self):
        if self.energy == 0 or self.energy > 9:
            return colored('0', 'red', attrs=["bold"])
        return str(self.energy)

    def __add__(self, other):
        self.energy += other


def load_grid(lines):
    grid = []
    nodes = []
    for line in lines:
        line = line.strip()
        if line:
            grid.append([Node(int(i)) for i in line])
            nodes += grid[-1]


    w = len(grid[0])
    h = len(grid)

    adj = [(-1, -1), (-1, 0), (0, -1), (-1, 1), (1, -1), (1, 1), (1, 0), (0, 1)]

    for y in range(h):
        for x in range(w):
            node = grid[y][x]
            for i, j in adj:
                xi = x + i
                yj = y + j
                if xi < 0 or xi >= w or yj < 0 or yj >= h:
                    continue
                else:
                    neb = grid[yj][xi]
                    node._edges.append(neb)
    return nodes, grid

def step(nodes, grid=None):
    for n in nodes:
        n += 1
    flashing = True
    if grid:
        print_grid(grid)
    while flashing:
        flashing = False
        for n in nodes:
            if n.energy > 9 and not n.flashed:
                n.flashed = True
                flashing = True
                for e in n.edges:
                    e += 1

                if grid:
                    print_grid(grid)
    cnt = 0
    for n in nodes:
        if n.flashed:
            cnt += 1
            n.energy = 0
            n.flashed = False
    if grid:
        print_grid(grid)
    return cnt

#p1
# nodes, grid = load_grid(lines)

# total = 0
# for s in range(100):
#     total += step(nodes)
#     sync = True
#     for n in nodes:
#         if n.energy != 0:
#             sync = False
#     if sync:
#         print('sync:', s+1)
# print(total)

#p2
nodes, grid = load_grid(lines)
# s = 0
# while True:
#     s += 1
#     step(nodes)
#     sync = True
#     for n in nodes:
#         if n.energy != 0:
#             sync = False
#     if sync:
#         print('sync:', s)
#         break


import time
nodes, grid = load_grid(lines)
for i in range(1000):
    step(nodes, grid)
    sync = True
    for n in nodes:
        if n.energy != 0:
            sync = False
    if sync:
        print('sync')
        break
