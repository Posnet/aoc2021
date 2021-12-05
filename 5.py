import sys, math
import termcolor
lines = sys.stdin.readlines()

segments = []
maxp = None
minp = None
for line in lines:
	p1, p2 = line.split(" -> ")
	x1, y1 = p1.split(',')
	x2, y2 = p2.split(',')
	x1,y1,x2,y2 = [int(z) for z in [x1, y1, x2, y2]]
	if not maxp:
		maxp = x1
	s = max([x1,y1,x2,y2])
	if  s > maxp:
		maxp = s
	if not minp:
		minp = x1
	p1 = (x1, y1)
	p2 = (x2, y2)
	segments.append(tuple(sorted((p1, p2))))
maxp = 10 ** round(math.log(maxp, 10))
grid = [[0] * maxp for _ in range(maxp)]
for ((x1, y1), (x2, y2) ) in segments:
	if (x1 == x2):
		for i in range(y1, y2+1):
			grid[i][x1] += 1
	elif (y1 == y2):
		for i in range(x1, x2+1):
			grid[y1][i] += 1
	else:
		yp = y1
		for x in range(x1, x2+1):
			grid[yp][x] += 1
			if y1 > y2:
				yp -= 1
			else:
				yp += 1



# for row in grid:
# 	row = ''.join([termcolor.colored(f'{i}', 'red') if i > 0 else str(i)  for i in row])
# 	print(row)

count = 0
for row in grid:
	for col in row:
		if col >= 2:
			count += 1

print(count)