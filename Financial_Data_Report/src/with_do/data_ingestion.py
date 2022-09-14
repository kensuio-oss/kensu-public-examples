# Import the libs and configure the (env) variables
import sys
import kensu.pandas as pd #regular pandas, monkey patched with data observability layer
from kensu.utils.kensu_provider import KensuProvider as K #import data observability client

month = sys.argv[1]
year = sys.argv[2]

# Initialize data observability client
k = K().initKensu(process_name="Data Ingestion")

# Core Script: Concatenate data sources in order to create a central repository: monthly_assets
Apple = pd.read_csv("../datasources/%s/%s/Apple.csv"%(year, month), parse_dates=['Date'], dtype={'Symbol':'category'})
Buzzfeed = pd.read_csv("../datasources/%s/%s/Buzzfeed.csv"%(year, month), parse_dates=['Date'], dtype={'Symbol':'category'})
EURUSD = pd.read_csv("../datasources/%s/%s/EURUSD.csv"%(year, month), parse_dates=['Date'], dtype={'Symbol':'category'})
Microsoft = pd.read_csv("../datasources/%s/%s/Microsoft.csv"%(year, month), parse_dates=['Date'], dtype={'Symbol':'category'})
iMetal = pd.read_csv("../datasources/%s/%s/iMetal.csv"%(year, month), parse_dates=['Date'], dtype={'Symbol':'category'})
AppTech = pd.read_csv("../datasources/%s/%s/AppTech.csv"%(year, month), parse_dates=['Date'], dtype={'Symbol':'category'})

monthly_assets = pd.concat([Apple, Buzzfeed, EURUSD, Microsoft, iMetal, AppTech]).astype({"Symbol": 'category'})
monthly_assets.to_csv("../datasources/%s/%s/monthly_assets.csv"%(year, month), index=False)
