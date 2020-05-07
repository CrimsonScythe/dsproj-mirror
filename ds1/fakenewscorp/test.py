from collections import defaultdict

lst = list()
d1 = {'a':2, 'b':4, 'c':8}
d2 = {'a':1, 'b':2, 'c':3, 'd':5}
d3 = {'a':0}

lst.append(d1)
lst.append(d2)
lst.append(d3)


max_dict=lst[1]
# print(max_dict)

for d in lst:
    if (d==max_dict):
        continue
    missing_keys = set(max_dict.keys()) - set(d.keys())
    for k in missing_keys:
        d[k] = 0

dd = defaultdict(list)

for d in lst: # you can list as many input dicts as you want here
    for key, value in d.items():
        dd[key].append(value)

print(dd)        