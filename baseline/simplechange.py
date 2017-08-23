import pandas as pd
from tqdm import *

r = open('test_replace.csv')
w = open('baseline19.txt','w')
hot_test = pd.read_pickle('../pkl/sort_test.pkl')
test = hot_test.sort_values('user_id', ascending=False)
# print(test)
for i in tqdm(r.readlines()):
    items = i.strip().split(',')[1].split(' ')
    user = i.strip().split(',')[0]
    flag = 0
    cate = {}
    for j in range(5):
        for k in test.index:
            if items[j] == k[1]:
                cate[k[0]] = 1
    # print(cate)
    for j in range(5):
        if items[j] == '558082':
            if flag == 1:
                for k in test.index:
                    # if k[1] == '557579':
                    #     continue
                    if k[1] not in items and k[0] not in cate:
                        items[j] = k[1]
                        break
                break
            else:
                flag += 1

    w.write('{0},{1}\n'.format(user, ' '.join(items)))