#Import the libs and configure the (env) variables

import urllib3
urllib3.disable_warnings()
import os
import shutil
os.environ['KSU_CONF_FILE']="../conf.ini"

import logging
logger = logging.getLogger('my-logger')
logger.propagate = False

import sys

month = sys.argv[1]
year = sys.argv[2]

# download kensu spark collector jar if doesn't exist in ../lib/
from spark_collector_downloader import maybe_download_spark_collector, kensu_agent_jar_local_path
maybe_download_spark_collector(kensu_agent_jar_local_path)


from pyspark.sql import SparkSession


#Inject Kensu agent in spark session
from kensu.pyspark import init_kensu_spark

#Inject Kensu agent in spark session: Add the path to the .jar to the SparkSession
spark = SparkSession.builder.appName("Example")\
    .config("spark.driver.extraClassPath", kensu_agent_jar_local_path)\
    .getOrCreate()
spark.sparkContext.setLogLevel("WARN")

#Inject Kensu agent in spark session: Link the spark job to Kensu
init_kensu_spark(spark,process_name="Reporting",compute_input_stats=False,output_stats_compute_std_dev=True,use_api_client=True)

#Core Script: Extract data from the monthly_assets data source and create 2 reports with a new column
all_assets = spark.read.option("inferSchema","true").option("header","true").csv("../datasources/%s/%s/monthly_assets.csv"%(year,month))

apptech = all_assets[all_assets['Symbol'] == 'APCX']
Buzzfeed = all_assets[all_assets['Symbol'] == 'BZFD']

buzz_report = Buzzfeed.withColumn('Intraday_Delta', Buzzfeed['Adj Close'] - Buzzfeed['Open'])
apptech_report = apptech.withColumn('Intraday_Delta', apptech['Adj Close'] - apptech['Open'])

kept_values = ['Open','Adj Close','Intraday_Delta']

final_report_buzzfeed = buzz_report[kept_values]
final_report_apptech = apptech_report[kept_values]

#We programmatically add a Variability rule on the report_AppTech data source

from kensu.utils.rule_engine import add_variability_constraint_data_source
add_variability_constraint_data_source('report_AppTech_csv',"Adj Close.mean",variation_in_percent=30)

from kensu.utils.kensu_provider import KensuProvider as K
k=K().instance()
k.send_rules()

# spark creates a directory instead of file, so use distinct name from .csv
final_report_buzzfeed.write.mode('overwrite').csv("../datasources/%s/%s/report_buzzfeed_csv"%(year,month))
final_report_apptech.write.mode('overwrite').csv("../datasources/%s/%s/report_AppTech_csv"%(year,month))

#Stop the Spark session after having sent the metadata
import time
time.sleep(30)
spark.stop()
