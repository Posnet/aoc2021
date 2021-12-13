import os
import sys
import termcolor
from sty import fg, bg, ef, rs
import time
from random import shuffle

lines = sys.stdin.readlines()

grid = []
global_id = 0

COLORS = list(termcolor.COLORS.keys())[1:]

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
    print(''.join(data))
    # time.sleep(0.2)


class Node:
    def __init__(self, height):
        global global_id
        self.idx = global_id
        global_id += 1
        self.height = height
        self._edges = []
        self.basin = None
        self.reached = False

    @property
    def edges(self):
        return self._edges

    @property
    def lowest(self):
        lowest = True
        for edge in self.edges:
            if edge <= self:
                lowest = False
        return lowest

    @property
    def risk(self):
        return self.height + 1

    def flood(self, idx):
        self.basin = idx
        self._frontier = set([self])
        self._basin = set()
        return self._basin

    def pump(self):
        if self._frontier:
            cand = list(self._frontier)
            n = cand[0]
            self._frontier = set(cand[1:])
            n.reached = True
            if n.height < 9 and n not in self._basin:
                self._basin.add(n)
                n.basin = self.basin
                self._frontier |= set(n.edges)
                self._basin.add(n)
        return len(self._frontier)

    def __le__(self, other):
        return self.height <= other.height

    def __eq__(self, other):
        return self.idx == other.idx

    def __hash__(self):
        return self.idx

    def __repr__(self):
        attrs = ''
        if self.lowest:
            attrs = ef.bold
        if self.basin is not None:
            return fg.white + bg(250 - (22 * self.risk), 10, 24 * self.risk) + attrs + '  ' + rs.all
        elif self.lowest:
            return fg.gree + str('  ') + rs.all
        elif self.height == 9:
            if self.reached:
                return bg(0, 0, 240) + '  ' + rs.all
            else:
                return('  ')
        else:
            return '  '
            return str(self.height)


nodes = []
for line in lines:
    line = line.strip()
    if line:
        grid.append([Node(int(i)) for i in line])
        nodes += grid[-1]


w = len(grid[0])
h = len(grid)

print(h, w)
print()

adj = [(-1, 0), (+1, 0), (0, -1), (0, +1)]

low_points = []
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


lowest = [n for n in nodes if n.lowest]


def flood(lowest, grid):
    basins = []
    shuffle(lowest)
    for idx, n in enumerate(lowest):
        basins.append(n.flood(idx))

    done = 1
    while done > 0:
        done = 0
        for n in lowest:
            done += n.pump()
        print_grid(grid)
    print_grid(grid)
    return basins


basins = flood(lowest, grid)

print(sum([n.risk for n in lowest]))
size = 1
for basin in sorted(basins, key=lambda x: len(x), reverse=True)[:3]:
    size *= len(basin)
print(size)
