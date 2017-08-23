import pandas as pd
import pickle



def create_and_save_item_id_dict():
    news_dict = {}
    index = 0
    all_news = pd.read_pickle('../pkl/process.all_news.pkl')
    print('all news:', all_news.shape)
    # print(all_news.values)
    news = pd.read_pickle('../pkl/process.news.pkl')
    print('news:', news.shape)

    for i in all_news.values:
        if i[0] not in news_dict:
            news_dict[i[0]] = index
            index += 1

    print('dict len:', news_dict.__len__())

    output = open('../pkl/dict.all_news.pkl', 'wb')
    pickle.dump(news_dict, output)
    output.close()

def create_and_save_user_id_dict():
    users_dict = {}
    index = 0
    train = pd.read_pickle('../pkl/process.train.pkl')
    for i in train.values:
        if i[0] not in users_dict:
            users_dict[i[0]] = index
            index += 1

    print('dict len:', users_dict.__len__())

    output = open('../pkl/dict.users.pkl', 'wb')
    pickle.dump(users_dict, output)
    output.close()

def create_and_save_candidates_list():
    with open('../raw/candidate.txt') as f:
        can = [x.strip() for x in f.readlines()]

    output = open('../pkl/list.candidate.pkl', 'wb')
    pickle.dump(can, output)
    output.close()

def create_user_item_dict():
    train = pd.read_csv('../raw/train.csv', delimiter=',')
    ui = {}
    for i in train.values:
        if i[0] not in ui:
            ui[i[0]] = {}
        ui[i[0]][i[1]] = 1

    print(ui)
    output = open('../pkl/dict.ui.pkl', 'wb')
    pickle.dump(ui, output)
    output.close()
# def create_and_save_test_matric():
#     users_dict, news_dict = ct.get_user_item_id_dict()
#     t = open('../raw/test.txt')
#     mat = np.zeros([users_dict.__len__(), news_dict.__len__()])
#     for line in t.readlines():
#         item = line.strip().split(',')
#         userid = item[0]
#         for news in item[1].split(' '):
#             mat[users_dict[userid], news_dict[int(news)]] = 1
#
#     return mat


if __name__ == '__main__':
    # create_and_save_candidates_list()
    # create_and_save_item_id_dict()
    # create_and_save_user_id_dict()
    # create_and_save_test_matric()
    # print(create_and_save_test_matric())
    create_user_item_dict()