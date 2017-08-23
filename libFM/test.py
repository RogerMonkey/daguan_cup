from pyfm import pylibfm
from sklearn.feature_extraction import DictVectorizer
import numpy as np
from sklearn.metrics import log_loss

action = {'view':1, 'deep_view' :2, 'collect':3, 'share':4, 'comment':5}
def loadData(filename):
    data = []
    y = []
    users = set()
    items = set()
    with open(filename) as f:
        f.readline()
        for line in f.readlines():
            (user, newid, cateid, actype, actime) = line.replace('"','').split(',')
            data.append({'user_id':user, 'newid':newid, 'cateod':cateid})
            # print(actype)
            y.append(action[actype])
            users.add(user)
            items.add(newid)

    return (data, np.array(y), users, items)





(train_data, y_train, train_users, train_items) = loadData('../raw/train.csv')
v = DictVectorizer()
X_train = v.fit_transform(train_data)

fm = pylibfm.FM(num_factors=10, num_iter=5, verbose=True, task="classification", initial_learning_rate=0.001, learning_rate_schedule="optimal")
fm.fit(X_train, y_train)
print("Validation log loss: %.4f" % log_loss(y_train,fm.predict(X_train)))