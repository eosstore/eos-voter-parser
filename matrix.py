
import requests
import json
import sys

dir = sys.argv[1]


top_50pbs = [""]*50
top_50voters = [""]*50
top_50voters_with_token = [""]*50
matrix = ""


# [u'bitfinexeos1', u'eoscanadacom', u'eosauthority', ....]
def get_top_50bps():
    global top_50pbs
    try:
        r = requests.post("http://127.0.0.1:8888/v1/chain/get_producers", '{"json":"true"}')
        if r.ok:
            ret = r.json()
            bps = ret["rows"]
            top50_ebp_names = list(map(lambda bp: bp["owner"], bps[:50]))
            top_50pbs = top50_ebp_names
            return top50_ebp_names
    except:
        pass
    return False


# [(u'ha2tsmzqhege', 117622704702), (u'gyzdcmjwgmge', 87499900000), (u'gyzdgmbqgage', 42966272100),...]
def get_top_50voters_with_token():
    global top_50voters, top_50voters_with_token
    d = {}
    for i in range(179):
        f_name = "list" + str(i + 1) + ".txt"
        f = open(dir + "/" + f_name)
        rows = json.load(f)
        for r in rows:
            if r['producers']:
                owner = r["owner"]
                stacked = int(r["staked"])
                d[owner] = stacked

    res = sorted(d.items(), key=lambda x: x[1], reverse=True)
    top_50voters_with_token = res[:50]
    i = 0
    for voter in top_50voters_with_token:
        top_50voters[i] = voter[0]
        i += 1


class Table:
    def __init__(self, row, col):
        self.matrix =  [[0 for i in range(col.__len__())] for j in range(row.__len__())]
        self.row = row
        self.col = col

    def get_row_n(self, name):
        n = 0
        for bp in self.row:
            if name == bp:
                return n
            else:
                n += 1

    def get_col_n(self, name):
        n = 0
        for voter in self.col:
            if name == voter:
                return n
            else:
                n += 1

    def set(self, col_name, row_name):
        self.matrix[self.get_row_n(row_name)][self.get_col_n(col_name)] = 1

    def dump(self):
        for row in self.matrix:
            res = ""
            for v in row:
                res += str(v) + " "
            print res


def get_matrix():
    global matrix
    matrix = Table(top_50pbs, top_50voters)
    for i in range(179):
        f_name = "list" + str(i + 1) + ".txt"
        f = open(dir + "/" + f_name)
        rows = json.load(f)
        for r in rows:
            if r['producers'] and r['owner'] in top_50voters:
                for bp in r['producers']:
                    if bp in top_50pbs:
                        matrix.set(r['owner'], bp)



if __name__ == '__main__':
    get_top_50bps()
    get_top_50voters_with_token()
    get_matrix()

    #dump
    for bp in top_50pbs:
        print bp

    str1 = ""
    str2 = ""
    for voter in top_50voters_with_token:
        str1 += voter[0] + " "
        str2 += str(voter[1]) + " "

    print str1
    print str2

    matrix.dump()



