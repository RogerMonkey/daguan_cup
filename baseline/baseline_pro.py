import common.process as cp
import common.tools as ct
import pandas as pd
from tqdm import tqdm
import numpy as np

can_limit = 20

cdt = ct.get_pickle('../pkl/list.candidate.pkl')
cate = pd.read_pickle('../pkl/baseline.pkl')

news = pd.read_pickle('../pkl/process.news.pkl')
readed = pd.read_pickle('../pkl/dict.ui.pkl')
hot_test = pd.read_pickle('../pkl/sort_test.pkl')
result = open('../result/baseline.txt', 'w')

def get_cate_list(df, cate):
    cate_new = {}
    for i in df.index:
        if i in cate:
            value = df.loc[i].values[0] * 1 \
                    + df.loc[i].values[1] * 2 \
                    + df.loc[i].values[2] * 3 \
                    + df.loc[i].values[3] * 3 \
                    + df.loc[i].values[4] * 3
            # if value > 3:
            cate_new[i] = value

    # if '1_1' in cate_new and '1_12' in cate_new:
    #     if cate_new['1_1'] == cate_new['1_12']:
    #         cate_new['1_1'] += 1
            # print(cate_new['1_1'], cate_new['1_12'], 'Ouch!!')
    # if '1_3' in cate_new and '1_6' in cate_new:
    #     if cate_new['1_3'] == cate_new['1_6']:
            # print(cate_new['1_3'], cate_new['1_6'], 'No!!')
            # cate_new['1_6'] += 1
    return cate_new


def ruozhipaixu(cate, can):
    # if len(can) == 0:
    #     print('Onno!!!')
    for i in cate:
        if i[1] in can:
            i[2] *= can[i[1]]

    cate = sorted(cate, key=lambda  x:x[2], reverse=True)
    # print(cate)
    return [x[0] for x in cate]

ltx = 0
for candidate in tqdm(cdt):
    # ltx += 1
    # if ltx >10:
    #     break
    history = cate.loc[candidate].sort_values('score', ascending=False)

    # print(cate_list)
    test = hot_test.sort_values('user_id', ascending=False)
    can = []
    can_cate = {}
    location_suffix = 10
    for i,j in zip(test.index, test.values):
        # if i[1] == '558578':
        #     continue
        can.append([i[1],i[0],j[0] + location_suffix])
        # print(i)
        if location_suffix != 0:
            location_suffix -= 1
        if i[0] not in can_cate:
            can_cate[i[0]] = 0
        if len(can) == can_limit:
            break
    # print(can)

    can_cate = get_cate_list(history, can_cate)
    # print(ruozhipaixu(can, can_cate))
    # print(can_cate)
    # print(can)
    final = ' '.join(ruozhipaixu(can, can_cate)[:5])
    final = final.replace('558331', 'Template_index')
    final = final.replace('558578','558331')
    final = final.replace('Template_index', '558578')
    final = final.replace('558578', '558082')

    final = final.split(' ')
    flag = 0
    for j in range(5):
        if final[j] == '558082':
            if flag == 1:
                for k in test.index:
                    if k[1] == '557579':
                        continue
                    if k[1] not in final:
                        final[j] = k[1]
                        break
                break
            else:
                flag += 1

    result.write('{0},{1}\n'.format(candidate, ' '.join(final)))
    # print(readed)
    # 只取评分最高的类别作为推荐结果
    # for cat_top in history.index:
    #     try:
    #         cat_news = hot_test.loc[cat_top].sort_values('user_id', ascending=False)
    #     except:
    #         continue
    #     # print(cat_news)
    #     limit = []
    #     for n in cat_news.index:
    #         item = n
    #         if item in readed[candidate]:
    #             print("hits!")
    #             continue
    #         limit.append(str(item))
    #
    #         if len(limit) == 5:
    #             break
    #
    #     if len(limit) == 5:
    #         break
    # result.write('{0},{1}\n'.format(candidate, ' '.join(limit)))

