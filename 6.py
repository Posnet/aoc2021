import sys
lines = sys.stdin.readlines()
fishes = [int(i) for i in lines[0].split(',')]

fishdex = [0] * 9

for fish in fishes:
    fishdex[fish] += 1

for i in range(256):
    new = fishdex[0]
    fishdex = fishdex[1:] + [new]
    fishdex[6] += new
print(sum(fishdex))

