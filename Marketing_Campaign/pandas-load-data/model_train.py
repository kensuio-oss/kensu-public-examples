import urllib3, datetime, sys
urllib3.disable_warnings()

from kensu.utils.kensu_provider import KensuProvider
k = KensuProvider().initKensu(project_names=["Marketing"],process_name='Python :: Model Train',input_stats=True)

import kensu.pickle as pickle
from kensu.sklearn.model_selection import train_test_split
import kensu.pandas as pd

from kensu.utils.kensu_provider import KensuProvider
KensuProvider().initKensu()


data = pd.read_csv("first_campaign/orders.csv")

df=data[['total_qty', 'total_basket']]

X = df.drop('total_basket',axis=1)
y = df['total_basket']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

from kensu.sklearn.linear_model import LinearRegression
model=LinearRegression().fit(X_train,y_train)

with open('model.pickle', 'wb') as f:
    pickle.dump(model,f)