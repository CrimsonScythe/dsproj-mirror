
v_list = list()
string = 'hello mello yello hello'
string2= 'hello mellow fello'
content = string.split()
print(content)
index=0
l = list()
for d in content:
    if d not in v_list:
        v_list.append(d)
        zList = [0]*4
        zList[index] = 1 
        l.append({'word': d, 'freq':zList})
    else:
        l_index = next((i for i, item in enumerate(l) if item['word'] == d), None)
        l[l_index]['freq'][index]=l[l_index]['freq'][index]+1    

    index+=1
print(l)        