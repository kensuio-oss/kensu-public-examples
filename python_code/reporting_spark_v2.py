

import urllib3
urllib3.disable_warnings()
import os
os.environ['CONF_FILE']="../conf.ini"

import logging
logger = logging.getLogger('my-logger')
logger.propagate = False

import sys

month = sys.argv[1]
year = sys.argv[2]

from pyspark.sql import SparkSession
from kensu.pyspark import init_kensu_spark


#Add the path to the .jar to the SparkSession
spark = SparkSession.builder.appName("Example")\
    .config("spark.driver.extraClassPath", "../lib/kensu-dam-spark-collector-0.17.2_spark-3.0.1.jar")\
    .getOrCreate()
spark.sparkContext.setLogLevel("OFF")

#Init Kensu

init_kensu_spark(spark,explicit_process_name = "Reporting",kensu_py_client=True)




all_assets = spark.read.option("inferSchema","true").option("header","true").csv("../datasources/%s/%s/monthly_assets.csv"%(year,month))

apptech = all_assets[all_assets['Symbol'] == 'APCX']
Buzzfeed = all_assets[all_assets['Symbol'] == 'BZFD']

buzz_report = Buzzfeed.withColumn('Intraday_Delta', Buzzfeed['Adj Close'] - Buzzfeed['Open'])
apptech_report = apptech.withColumn('Intraday_Delta', apptech['Adj Close'] - apptech['Open'])

kept_values = ['Open','Adj Close','Intraday_Delta']


final_report_buzzfeed = buzz_report[kept_values]
final_report_apptech = apptech_report[kept_values]

from kensu.utils.rule_engine import add_variability_constraint_data_source
add_variability_constraint_data_source('report_AppTech.csv',"Adj Close.mean",variation_in_percent=30)

from kensu.utils.kensu_provider import KensuProvider as K
k=K().instance()
k.send_rules()

final_report_buzzfeed.write.mode('overwrite').csv("../datasources/%s/%s/report_buzzfeed.csv"%(year,month))
final_report_apptech.write.mode('overwrite').csv("../datasources/%s/%s/report_AppTech.csv"%(year,month))


import time
time.sleep(30)
spark.stop()