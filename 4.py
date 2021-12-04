import sys
from termcolor import colored
lines = sys.stdin.read().strip().split('\n')

class Board:
	def __init__(self, data, width):
		self.data = data
		self.width = width
		self._winners = None
		self.numbers = []

	def __repr__(self):
		res = []
		for i in range(self.width):
			start = self.width * i
			end = (self.width * (i + 1)) 
			row = []
			for d in self.data[start:end]:
				if d in self.numbers:
					row.append(colored(f'{d:>2}', 'green'))
				else:
					row.append(f'{d:>2}')
			res.append(' '.join(row))
		return '\n'.join(res)

	@property
	def columns(self):
		res = []
		for i in range(self.width):
			res.append([d for d in self.data[i::self.width]])
		return res

	@property
	def rows(self):
		res = []
		for i in range(self.width):
			start = self.width * i
			end = (self.width * (i + 1)) 
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
			ndata = [int(i) for i in line.strip().split(' ') if i]
			if not width:
				width = len(ndata)
			data  += ndata
		else:
			if data:
				boards.append(Board(data, width))
			width = None
			data = []
	if data:
		boards.append(Board(data, width))
	return boards

def find_winner(numbers, boards):
	all_winners = []
	for idx, b in enumerate(boards):
		for w in b.winners:
			all_winners.append((w, idx))
	called = set()
	for n in numbers:
		called.add(n)
		for w, idx in all_winners:
			if w.issubset(called):
				b = boards[idx]
				print(w)
				unmarked = sum(set(b.data) - called)
				score = unmarked * n
				b.numbers = called
				return called, b, score

numbers = [int(i) for i in lines[0].split(',')]
boards = get_boards(lines)
called, board, score = find_winner(numbers, boards)
print(called)
print(board)
print(f'Score:{score}')