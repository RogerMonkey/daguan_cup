import common.process as cp
import common.tools as ct
import pandas as pd
from tqdm import tqdm
import numpy as np

ruozhizidian = {'557579':'1_6', '558082':'1_11', '558788':'1_6', '557167':'1_6', '558910':'1_1',
                '556664':'1_8', '552472' : '1_2', '555820' : '1_6','558077' : '1_5', '557018' : '1_6'}

cdt = ct.get_pickle('../pkl/list.candidate.pkl')
cate = pd.read_pickle('../pkl/baseline.pkl')
# train = pd.read_pickle('../pkl/process.train.pkl')[['user_id', 'item_id']]

news = pd.read_pickle('../pkl/process.news.pkl')
readed = pd.read_pickle('../pkl/dict.ui.pkl')
hot_test = pd.read_pickle('../pkl/sort_test.pkl')
result = open('rogerbase.txt', 'w')

def get_cate_list(df):
    cate_list = []
    for i in df.index:
        # if i in ['1_1','1_6','1_11']:
        if i in ['1_1','1_6','1_11','1_2','1_5','1_8']:
            cate_list.append([i, df.loc[i].values[5]])

    return cate_list


def ruozhipaixu(cate, predict):
    # if len(cate) == 3:
    #     if cate[1][1] / cate[0][1] > 0.8 and cate[2][1] / cate[0][1] < 0.8:
    #         cate = [cate[0], cate[2]]

    # 过滤过低的item cate
    # cate_t = []
    # for i in cate:
    #     if i[1] < 3:
    #         continue
    #     cate_t.append(i)
    # cate = cate_t

    if len(cate) == 0:
        print('Ouch!!')
        return predict[:5]
    elif len(cate) == 1:
        new = ['','','','','','','','','','']
        idx = 0
        cdx = 0
        cate_id = cate[0][0]
        # print('Single',cate_id)
        # if cate[0][1] < 20:
        #     return new

        for i in range(10):
            if ruozhizidian[predict[i]] == cate_id:
                cdx += 1
        for i in range(10):
            if ruozhizidian[predict[i]] == cate_id:
                new[idx] = predict[i]
                idx += 1
            else:
                new[cdx] = predict[i]
                cdx += 1
        return new[:5]
    elif len(cate) == 2:
        new = ['','','','','','','','','','']
        idx = 0
        cdx = 0
        fdx = 0
        cat1 = cate[0]
        cat2 = cate[1]

        # print('Double', cat1[0], cat2[0])
        if cat1[1] > 18 and cat2[1]/cat1[1] < 0.8:
        #     print('Double')
            for i in range(10):
                if ruozhizidian[predict[i]] == cat1[0]:
                    cdx += 1
                    fdx += 1
                if ruozhizidian[predict[i]] == cat2[0]:
                    fdx += 1
            for i in range(10):
                if ruozhizidian[predict[i]] == cat1[0]:
                    new[idx] = predict[i]
                    idx += 1
                elif ruozhizidian[predict[i]] == cat2[0]:
                    new[cdx] = predict[i]
                    cdx+=1
                else:
                    new[fdx] = predict[i]
                    fdx += 1
            return new[:5]
        # for i in range(5):
        #         if ruozhizidian[predict[i]] == '1_6':
        #             new[idx] = predict[i]
        #             idx += 1
        #         elif ruozhizidian[predict[i]] == '1_1':
        #             new[3] = predict[i]
        #         else:
        #             new[4] = predict[i]
        return predict[:5]
    elif len(cate) == 3:
        # print('Triple')
        new = ['','','','','','','','','','']
        idx = 0
        cdx = 0
        fdx = 0
        cat1 = cate[0]
        cat2 = cate[1]
        cat3 = cate[2]
        if cat1[1] > 18 and cat2[1] / cat1[1] < 0.8 and cat3[1] / cat2[1] < 0.8:
            print('Triple')
            for i in range(10):
                if ruozhizidian[predict[i]] == cat1[0]:
                    cdx += 1
                    fdx += 1
                if ruozhizidian[predict[i]] == cat2[0]:
                    fdx += 1

            for i in range(10):
                if ruozhizidian[predict[i]] == cat1[0]:
                    new[idx] = predict[i]
                    idx += 1
                elif ruozhizidian[predict[i]] == cat2[0]:
                    new[cdx] = predict[i]
                    cdx+=1
                elif ruozhizidian[predict[i]] == cat3[0]:
                    new[fdx] = predict[i]
                    fdx += 1
            return new[:5]
        return predict[:5]
    else:
        return predict[:5]
ltx = 0
for candidate in tqdm(cdt):
    # ltx += 1
    # if ltx >10:
    #     break
    history = cate.loc[candidate].sort_values('score', ascending=False)
    cate_list = get_cate_list(history)
    # print(cate_list)
    test = hot_test.sort_values('user_id', ascending=False)
    limit = []
    for i in test.index:
        limit.append(i[1])
        if len(limit) == 10:
            break
    result.write('{0},{1}\n'.format(candidate, ' '.join(ruozhipaixu(cate_list, limit))))
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

