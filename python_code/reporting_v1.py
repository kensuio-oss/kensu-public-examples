

import urllib3
urllib3.disable_warnings()
import os
os.environ['CONF_FILE']="../conf.ini"

import sys

month = sys.argv[1]
year = sys.argv[2]

from kensu.utils.kensu_provider import KensuProvider as K
k = K().initKensu(process_name="Reporting",get_code_version = lambda : 'v1',input_stats=False)

import kensu.pandas as pd
pd.options.mode.chained_assignment = None

all_assets = pd.read_csv("../datasources/%s/%s/monthly_assets.csv"%(year,month),parse_dates=['Date'])

apptech = all_assets[all_assets['Symbol'] == 'APCX']                
Buzzfeed = all_assets[all_assets['Symbol'] == 'ENFA']   

Buzzfeed['Intraday_Delta'] = Buzzfeed['Adj Close'] - Buzzfeed['Open']
apptech['Intraday_Delta'] = apptech['Adj Close'] - apptech['Open']

kept_values = ['Open','Adj Close','Intraday_Delta']

Buzzfeed[kept_values].to_csv("../datasources/%s/%s/report_buzzfeed.csv"%(year,month),index=False)
apptech[kept_values].to_csv("../datasources/%s/%s/report_AppTech.csv"%(year,month),index=False)