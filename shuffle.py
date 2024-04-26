import random

with open("./adj.txt", "r") as r:
    adjs = r.readlines()

random.shuffle(adjs)

with open("res.txt", "w") as w:
    w.write("".join(adjs))
