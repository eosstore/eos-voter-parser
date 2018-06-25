
import json

f = open("data/v.json")

rows = json.load(f)


class Ticket:
    def __init__(self, voter, staked, last_vote_weight):
        self.voter = voter
        self.staked = staked
        self.last_vote_weight = last_vote_weight

class






for r in rows:
    if r['producers'] != []:
        pass


