import sys
from collections import Counter
from tqdm.auto import tqdm
lines = sys.stdin.readlines()

template = lines[0].strip()

rules = {}
for line in lines[1:]:
    line = line.strip()
    if line:
        left, right = line.split(' -> ')
        rules[left] = right

print(template)
print(rules)

pairs = []
for i in range(len(template) - 1):
    pairs.append(template[i:i+2])

pairs = Counter(pairs)

for i in range(40):
    out = {}
    for p,c in pairs.items():
        for pp in (p[0] + rules[p], rules[p] + p[1]):
            cc = out.get(pp, 0)
            out[pp] = cc + c
    pairs = out
    print(pairs)

counts  = []       
for c in set(''.join(pairs.keys())):
    m1 = sum(count for p,count in pairs.items() if p[0] == c)
    m2 = sum(count for p,count in pairs.items() if p[1] == c)
    counts.append(max(m1, m2))

print(max(counts) - min(counts))