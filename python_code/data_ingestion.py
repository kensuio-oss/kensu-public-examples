
import urllib3
urllib3.disable_warnings()
import os
os.environ['CONF_FILE']="../conf.ini"


import sys

month = sys.argv[1]
year = sys.argv[2]


from kensu.utils.kensu_provider import KensuProvider as K   
k = K().initKensu(process_name="Data Ingestion")

import kensu.pandas as pd

Apple = pd.read_csv("../datasources/%s/%s/Apple.csv"%(year,month),parse_dates=['Date'])
Buzzfeed = pd.read_csv("../datasources/%s/%s/Buzzfeed.csv"%(year,month),parse_dates=['Date'])
EURUSD = pd.read_csv("../datasources/%s/%s/EURUSD.csv"%(year,month),parse_dates=['Date'])
Microsoft = pd.read_csv("../datasources/%s/%s/Microsoft.csv"%(year,month),parse_dates=['Date'])
iMetal = pd.read_csv("../datasources/%s/%s/iMetal.csv"%(year,month),parse_dates=['Date'])
AppTech = pd.read_csv("../datasources/%s/%s/AppTech.csv"%(year,month),parse_dates=['Date'])


monthly_assets = pd.concat([Apple,Buzzfeed,EURUSD,Microsoft,iMetal,AppTech])

monthly_assets.to_csv("../datasources/%s/%s/monthly_assets.csv"%(year,month),index=False)