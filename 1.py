import sys
import pandas as pd

data = [int(i) for i in sys.stdin.readlines()]
print(len(data))
cnt = 0
prev = None
for line in data:
    if prev:
        if line > prev:
            cnt += 1
    prev = line
print(cnt)


cnt = 0
prev = None
for line in range(len(data) - 2):
    window = data[line : line + 3]
    window = sum(window)
    if prev:
        if window > prev:
            cnt += 1
    prev = window
print(cnt)
