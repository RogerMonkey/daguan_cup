import numpy as np
import pandas as pd
import pickle

def get_pickle(path):
    input = open(path, 'rb')
    data = pickle.load(input)
    return data

def get_user_item_id_dict():
    return get_pickle('../pkl/dict.users.pkl')\
        ,get_pickle('../pkl/dict.all_news.pkl')

