# Import the libs and configure the (env) variables
import sys
import kensu.pandas as pd
pd.options.mode.chained_assignment = None
from kensu.utils.kensu_provider import KensuProvider as K

month = sys.argv[1]
year = sys.argv[2]

# Initialize Kensu tracking
k = K().initKensu(process_name="Reporting", get_code_version = lambda : 'v1', input_stats=False)

# Core Script: Extract data from the monthly_assets data source and create 2 reports with a new column
all_assets = pd.read_csv("../datasources/output/monthly_assets.csv", parse_dates=['Date'])

apptech = all_assets[all_assets['Symbol'] == 'APCX']                
Buzzfeed = all_assets[all_assets['Symbol'] == 'ENFA']   

Buzzfeed['Intraday_Delta'] = Buzzfeed['Adj Close'] - Buzzfeed['Open']
apptech['Intraday_Delta'] = apptech['Adj Close'] - apptech['Open']

kept_values = ['Date', 'Open', 'Adj Close', 'Intraday_Delta']

Buzzfeed[kept_values].to_csv("../datasources/report/buzzfeed.csv", index=False)
apptech[kept_values].to_csv("../datasources/report/AppTech.csv", index=False)