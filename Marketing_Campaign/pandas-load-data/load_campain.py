import urllib3, sys
urllib3.disable_warnings()

from kensu.utils.kensu_provider import KensuProvider
k = KensuProvider().initKensu(project_name="Marketing",process_name='Python :: Data_Load',compute_input_stats=True)


import kensu.pandas as pd
from sqlalchemy import create_engine

campaign = sys.argv[1]

customers = pd.read_csv(campaign+"_campaign/customer_list.csv")
engine = create_engine('postgresql://postgres:postgresPass@host.docker.internal:5432/testme')
customers.to_sql('customers', engine,index=False,if_exists='replace')
orders = pd.read_csv(campaign+"_campaign/orders.csv")
orders = orders.rename(columns={'id':"customer_id"})
orders.to_sql('orders', engine,index=False,if_exists='replace')
