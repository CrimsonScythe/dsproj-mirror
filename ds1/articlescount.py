import pandas as pd
import numpy as np
from cleantext import clean
from datetime import datetime
import datefinder
import re
import csv
import psycopg2












conn = psycopg2.connect(host = "localhost", dbname="postgres", user="postgres", password="root")
cur = conn.cursor() 
cur.execute('SELECT DISTINCT type_name FROM type;')
types = cur.fetchall()
# print(types)

cur.execute('SELECT DISTINCT domain_url FROM domain;')
domains = cur.fetchall()
# print(domains)

for o in domains:
    for p in types:
        if (p[0] != 'NULL'):
            domain=o[0]
            typ=p[0]
            cur.execute('SELECT COUNT(*) FROM domain, type WHERE domain_url=%s AND type_name=%s;', (domain, typ))
            count = cur.fetchall()
            # print(count[0])
            cur.execute('INSERT INTO articlescount VALUES (%s, %s, %s);', (o, p, count[0]))

conn.commit()
cur.close()
            # print(p[0])

            # print(o[0])
# print(type(types))

# cur.copy_from(f, 'articlescount', sep=',')
# conn.commit()
# cur.close()