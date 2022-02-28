

import urllib3
urllib3.disable_warnings()
import os
import sys
os.environ['CONF_FILE']="../conf.ini"
import logging
logging.basicConfig(stream=sys.stdout, level=logging.CRITICAL)


month = sys.argv[1]
year = sys.argv[2]

from pyspark.sql import SparkSession
from kensu.pyspark import init_kensu_spark


#Add the path to the .jar to the SparkSession
spark = SparkSession.builder.appName("Example")\
    .config("spark.driver.extraClassPath", "../lib/kensu-dam-spark-collector-0.17.2_spark-3.0.1.jar")\
    .getOrCreate()


#Init Kensu

init_kensu_spark(spark,explicit_process_name = "Reporting",input_stats=False,kensu_py_client=True)


all_assets = spark.read.option("inferSchema","true").option("header","true").csv("../datasources/%s/%s/monthly_assets.csv"%(year,month))

apptech = all_assets[all_assets['Symbol'] == 'APCX']
Buzzfeed = all_assets[all_assets['Symbol'] == 'ENFA']

buzz_report = Buzzfeed.withColumn('Intraday_Delta', Buzzfeed['Adj Close'] - Buzzfeed['Open'])
apptech_report = apptech.withColumn('Intraday_Delta', apptech['Adj Close'] - apptech['Open'])

kept_values = ['Open','Adj Close','Intraday_Delta']


final_report_buzzfeed = buzz_report[kept_values]
final_report_apptech = apptech_report[kept_values]

final_report_buzzfeed.write.mode('overwrite').csv("../datasources/%s/%s/report_buzzfeed.csv"%(year,month))
final_report_apptech.write.mode('overwrite').csv("../datasources/%s/%s/report_AppTech.csv"%(year,month))


import time
time.sleep(30)
spark.stop()