import sys
from termcolor import colored

lines = sys.stdin.read().strip().split("\n")


class Board:
    def __init__(self, data, width):
        self.data = data
        self.width = width
        self._winners = None
        self.called = []

    def __repr__(self):
        res = []
        for i in range(self.width):
            start = self.width * i
            end = self.width * (i + 1)
            row = []
            for d in self.data[start:end]:
                if d in self.called:
                    row.append(colored(f"{d:>2}", "green"))
                else:
                    row.append(f"{d:>2}")
            res.append(" ".join(row))
        return "\n".join(res)

    @property
    def score(self):
        unmarked = sum(set(self.data) - set(self.called))
        score = unmarked * self.called[-1]
        return score

    @property
    def columns(self):
        res = []
        for i in range(self.width):
            res.append([d for d in self.data[i :: self.width]])
        return res

    @property
    def rows(self):
        res = []
        for i in range(self.width):
            start = self.width * i
            end = self.width * (i + 1)
            res.append([d for d in self.data[start:end]])
        return res

    @property
    def winners(self):
        if not self._winners:
            winners = [set(w) for w in self.rows + self.columns]
            self._winners = winners
        return self._winners


def get_boards(lines):
    boards = []
    width = None
    data = []
    for line in lines[1:]:
        if line:
            ndata = [int(i) for i in line.strip().split(" ") if i]
            if not width:
                width = len(ndata)
            data += ndata
        else:
            if data:
                boards.append(Board(data, width))
            width = None
            data = []
    if data:
        boards.append(Board(data, width))
    return boards


def find_winner(numbers, boards, first):
    all_winners = []
    for idx, b in enumerate(boards):
        for w in b.winners:
            all_winners.append((w, idx))
    boards = dict(enumerate(boards))
    winners = {}
    called = set()
    for nidx, n in enumerate(numbers):
        called.add(n)
        for w, idx in all_winners:
            if w.issubset(called):
                if idx not in winners:
                    b = boards[idx]
                    b.called = numbers[: nidx + 1]
                    winners[idx] = b
    return winners


numbers = [int(i) for i in lines[0].split(",")]
boards = get_boards(lines)
winners = find_winner(numbers, boards, True)
first = list(winners.values())[0]
last = list(winners.values())[-1]
print(first)
print("Score:", first.score)
print()
print(last)
print("Score:", last.score)
print()
