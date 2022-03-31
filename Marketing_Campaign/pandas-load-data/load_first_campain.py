import urllib3, datetime
urllib3.disable_warnings()

from kensu.utils.kensu_provider import KensuProvider
k = KensuProvider().initKensu(project_names=["Marketing"],process_name='Python :: Data_Load',input_stats=True)


import kensu.pandas as pd
from sqlalchemy import create_engine

customers = pd.read_csv("first_campaign/customer_list.csv")
engine = create_engine('postgresql://postgres:postgresPass@host.docker.internal:5432/testme')
customers.to_sql('customers', engine,index=False,if_exists='replace')
orders = pd.read_csv("first_campaign/orders.csv")
orders = orders.rename(columns={'id':"customer_id"})
orders.to_sql('orders', engine,index=False,if_exists='replace')
