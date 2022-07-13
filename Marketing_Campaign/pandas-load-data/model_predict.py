

import kensu.pandas as pd
from kensu.utils.kensu_provider import KensuProvider
KensuProvider().initKensu()


data = pd.read_csv("/Users/sammykensu/KensuTools/kensu-public-examples/Marketing_Campaign/pandas-load-data/second_campaign/orders.csv")
df=data[['total_qty']]

import kensu.pickle as pickle
with open('model.pickle', 'rb') as f:
    model=pickle.load(f)

pred = model.predict(df)

data['model_pred']=pred

data.to_csv('model_tr.csv',index=False)
