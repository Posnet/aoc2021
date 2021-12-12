import sys
lines = sys.stdin.readlines()


class Node:
    def __init__(self, idx):
        self.idx = idx
        self._edges = set()
        if idx.isupper():
            self.large = True
        else:
            self.large = False
        if idx in ('start', 'end'):
            self.terminal = True

    def __hash__(self):
        return hash(self.idx)

    def __eq__(self, other):
        return self.idx == other.idx

    @property
    def small(self):
        res = (not self.large) and (self.idx != 'start') and (self.idx != 'end')
        return res

    def add_edge(self, node):
        if node.idx == 'start':
            return
        self._edges.add(node)

    def key(self):
        if self.idx == 'end':
            return 0
        else:
            total = 0
            for c in self.idx:
                total += ord(c)
            return total

    @property
    def edges(self):
        return self._edges
        # return sorted(list(self._edges), key=lambda x: x.key(), reverse=True)

    def __repr__(self):
        return f'Node({self.idx})'


def load(lines):
    start = None
    end = None
    nodes = {}

    for line in lines:
        line = line.strip()
        if line:
            left,right = line.split('-')
            if left in nodes:
                lnode = nodes[left]
            else:
                lnode = Node(left)
                nodes[left] = lnode
            if right in nodes:
                rnode = nodes[right]
            else:
                rnode = Node(right)
                nodes[right] = rnode
            lnode.add_edge(rnode)
            rnode.add_edge(lnode)

    for n in nodes.values():
        if n.idx == 'start':
            start = n
        elif n.idx == 'end':
            end = n

    return start, end, nodes

def small_check(e, path):
    res = False
    if e.small:
        smalls = {}
        for p in path:
            if p.small:
                if p in smalls:
                    smalls[p] += 1
                else:
                    smalls[p] = 1
        if max(smalls.values()) == 1:
            if smalls[e] == 1:
                res = True
    return res

def walk(start, end):
    paths = [[start]]
    while paths:
        path = paths.pop()
        if path[-1] == end:
            yield path
        else:
            for e in path[-1].edges:
                if ((e not in path) or e.large) or small_check(e, path):
                    np = path.copy()
                    np.append(e)
                    paths.append(np)



start, end, nodes = load(lines)

ctr = 0
for path in walk(start, end):
    ctr += 1
print(ctr)
