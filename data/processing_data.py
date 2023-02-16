import pandas as pd
from pandas import read_csv

"""Read data"""
ratings = read_csv("./ml-latest/ratings.csv")
print(ratings.head(5))


"""List userId"""
list_userId= ratings.userId.unique()
print(list_userId)


import pandas as pd
def splitData (userId):
    ratingUser01 = ratings[ratings.userId==userId]
    n_ratingUser01 = len(ratingUser01)
    ratingUser01_sorted = ratingUser01.sort_values(by=['timestamp'])
    n_train = int(round((n_ratingUser01*0.6),0))

    n_val = int(round((n_ratingUser01 - n_train)/2,0))
    n_test = n_ratingUser01 - n_train - n_val

    data_trainUserId = ratingUser01_sorted.head(n_train)
    data_valUserId = ratingUser01_sorted[n_train:n_train+n_val]
    data_testUserId = ratingUser01_sorted[n_train+n_val:]
    return [data_trainUserId, data_valUserId, data_testUserId]

data_train, data_val, data_test = splitData(1)
import numpy as np
list_userId = np.delete(list_userId, 0)
print(list_userId)
for userId in list_userId:
    data_trainUserId, data_valUserId, data_testUserId= splitData(userId)
    data_train = pd.concat([data_train, data_trainUserId], ignore_index=True)
    data_val = pd.concat([data_val, data_valUserId], ignore_index=True)
    data_test = pd.concat([data_test, data_testUserId], ignore_index=True)
data_train.to_csv('train_lastest_2.csv')
data_val.to_csv('val_lastest_2.csv')
data_test.to_csv('test_lastest_2.csv')
