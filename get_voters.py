import json
import sys

d = {}
dir = sys.argv[1]

for i in range(179):
    fname = "list" + str(i + 1) + ".txt"
    f = open(dir + "/" + fname)
    rows = json.load(f)
    for r in rows:
        if "eosstorebest" in r['producers']:
            # print r["owner"] + "   " + str(r["staked"]) + "  " + r["last_vote_weight"]
            owner = r["owner"]
            stacked = int(r["staked"])
            d[owner] = stacked


res = sorted(d.items(), key=lambda x: x[1], reverse=True)

for j in res:
    if int(j[1]) > 1000000000:
        print j[0] + "  " + str(j[1])













