import urllib3, datetime, sys
urllib3.disable_warnings()

from kensu.utils.kensu_provider import KensuProvider
k = KensuProvider().initKensu(project_names=["Marketing"],process_name='Python :: Model Predict',input_stats=True)

import kensu.pandas as pd

data = pd.read_csv("second_campaign/orders.csv")
df=data[['total_qty']]

import kensu.pickle as pickle
with open('model.pickle', 'rb') as f:
    model=pickle.load(f)

pred = model.predict(df)

data['model_pred']=pred

data.to_csv('model_tr.csv',index=False)
