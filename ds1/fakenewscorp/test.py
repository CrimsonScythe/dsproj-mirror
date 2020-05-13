from collections import defaultdict
import numpy as np
import psycopg2


sett = set()

sett.add("a")
sett.add("b")
sett.add("c")
sett.add("d")
sett.add("e")
sett.add("f")

dic = {k: v for v, k in enumerate(sett)}
print(dic['b'])