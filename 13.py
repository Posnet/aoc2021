import sys
from PIL import Image
lines = sys.stdin.readlines()

def print_grid(grid):
    # img = Image.new( 'RGB', (len(grid[0]),len(grid)), "black") # Create a new black image
    # pixels = img.load() # Create the pixel map
    # for i in range(img.size[0]):    # For every pixel:
    #     for j in range(img.size[1]):
    #         if grid[j][i]:
    #             pixels[i,j] = (255, 255, 255)
    #         else:
    #             pixels[i,j] = (0,0,0)
    # img.show()
    for row in grid:
        print(' '.join(['#' if i else '.' for i in row]))

fprefix = 'fold along'
points = []
folds = []
for line in lines:
    line = line.strip()
    if line:
        if line.startswith(fprefix):
            line = line[len(fprefix):].strip().split('=')
            folds.append((line[0], int(line[1])))
        else:
            line = line.split(',')
            x,y = int(line[0]), int(line[1])
            points.append((x, y))
h = None
w = None
for axis, idx in folds:
    if h is None and axis == 'y':
        h = (idx*2) + 1
    if w is None and axis == 'x':
        w = (idx*2) + 1
    if w and h:
        break
print(w, h)

grid = [[0] * w for _ in range(h) ]
for x,y in points:
    grid[y][x] += 1
print(w, h)
print(folds)

def merge(pre, rem):
    for y in range(len(rem)):
        for x in range(len(rem[y])):
            pre[y][x] += rem[y][x]
    return pre

def visible(grid):
    ctr = 0
    for row in grid:
        for cell in row:
            if cell:
                ctr += 1
    return ctr

for axis, idx in folds:
    if axis == 'x':
        pre = []
        rem = []
        offset = len(grid[0]) % 2
        for row in grid:
            pre.append(row[:idx])
            rem.append(row[idx+offset:][::-1])
        grid = merge(pre, rem)
    elif axis == 'y':
        offset = len(grid) % 2
        pre = grid[:idx]
        rem = grid[idx+offset:][::-1]
        grid = merge(pre, rem)
    else:
        raise ValueError('Unknown Axis')

print_grid(grid)
print('visible:', visible(grid))
