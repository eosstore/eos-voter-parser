
import sys

d1 = open(sys.argv[1])
d2 = open(sys.argv[2])

dict1 = {}
set1 = set()
dict2 = {}
set2 = set()

for line in d1:
    if line != "\n":
        item = line.strip("\n").split("  ")
        dict1[item[0]] = item[1]
        set1.add(item[0])

for line in d2:
    if line != "\n":
        item = line.strip("\n").split("  ")
        dict2[item[0]] = item[1]
        set2.add(item[0])

newvoter = set2 - set1
unvoter = set1 - set2

if sys.argv[3] == "unvoter":
    for unv in unvoter:
        print unv + " " + dict1[unv]
else:
    for v in newvoter:
        print v + " " + dict2[v]





