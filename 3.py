import sys
from collections import Counter

data = sys.stdin.read().strip().split()
stride = len(data[0])

def get_counters(data, stride):
	sdata = ''.join(data)
	counters = []
	for i in range(stride):
		counters.append(Counter(sdata[i::stride]))
	return [sorted(c.items(), key=lambda item: item[1]) for c in counters]

counters = get_counters(data, stride)
gamma = ''
eppsilon = ''
for c in counters:
	gamma += c[1][0]
	eppsilon += c[0][0]

print(int(gamma, 2)  * int(eppsilon, 2))

lst = list(data)

ctrs = get_counters(lst, stride)
for i in range(stride):
	if ctrs[i][0][1] == ctrs[i][1][1]:
		c = '1'
	else:
		c = ctrs[i][1][0]
	lst = [l for l in lst if l[i] == c]
	if len(lst) == 1:
		ox = int(lst[0], 2)
		break
	ctrs = get_counters(lst, stride)

lst = list(data)
ctrs = get_counters(lst, stride)
for i in range(stride):
	if ctrs[i][0][1] == ctrs[i][1][1]:
		c = '0'
	else:
		c = ctrs[i][0][0]
	lst = [l for l in lst if l[i] == c]
	if len(lst) == 1:
		co2 = int(lst[0], 2)
		break
	ctrs = get_counters(lst, stride)

print(ox * co2)