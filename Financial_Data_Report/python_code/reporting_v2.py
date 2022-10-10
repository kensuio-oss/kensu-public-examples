#Import the libs and configure the (env) variables

import urllib3
urllib3.disable_warnings()

import os
os.environ['KSU_CONF_FILE']="../conf.ini"
import sys

month = sys.argv[1]
year = sys.argv[2]

#Initialize Kensu tracking
from kensu.utils.kensu_provider import KensuProvider as K
k = K().initKensu(process_name="Reporting",get_code_version = lambda : 'v1',compute_input_stats=False)

#Inject Kensu agent in pandas library
import kensu.pandas as pd
pd.options.mode.chained_assignment = None

#Core Script: Extract data from the monthly_assets data source and create 2 reports with a new column
all_assets = pd.read_csv("../datasources/%s/%s/monthly_assets.csv"%(year,month),parse_dates=['Date'])

apptech = all_assets[all_assets['Symbol'] == 'APCX']                
Buzzfeed = all_assets[all_assets['Symbol'] == 'BZFD']   

Buzzfeed['Intraday_Delta'] = Buzzfeed['Adj Close'] - Buzzfeed['Open']
apptech['Intraday_Delta'] = apptech['Adj Close'] - apptech['Open']

kept_values = ['Open','Adj Close','Intraday_Delta']


#We programmatically add a Variability rule on the report_AppTech data source
from kensu.utils.rule_engine import add_variability_constraint_data_source
add_variability_constraint_data_source('report_AppTech.csv',"Adj Close.mean",variation_in_percent=30)

Buzzfeed[kept_values].to_csv("../datasources/%s/%s/report_buzzfeed.csv"%(year,month),index=False)
apptech[kept_values].to_csv("../datasources/%s/%s/report_AppTech.csv"%(year,month),index=False)

# Cleanup the metadata
os.remove("../datasources/%s/%s/report_buzzfeed.csv"%(year,month))
os.remove("../datasources/%s/%s/report_AppTech.csv"%(year,month))