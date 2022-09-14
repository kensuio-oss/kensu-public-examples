# Import the libs and configure the (env) variables
import sys
from pyspark.sql import SparkSession
import time
from kensu.pyspark import init_kensu_spark # Import Spark Data Observability Agent

month = sys.argv[1]
year = sys.argv[2]

# Inject Kensu agent in spark session: Add the path to the .jar to the SparkSession
spark = SparkSession.builder.appName("Example")\
    .config("spark.driver.extraClassPath", "../lib/kensu-dam-spark-collector-0.17.3_spark-3.0.1.jar")\
    .getOrCreate()
spark.sparkContext.setLogLevel("OFF")

# Inject Kensu agent in spark session: Link the spark job to Kensu
init_kensu_spark(spark, explicit_process_name = "Reporting", input_stats=False, kensu_py_client=True)

# Core Script: Extract data from the monthly_assets data source and create 2 reports with a new column
all_assets = spark.read.option("inferSchema", "true").option("header", "true")\
                    .csv("../datasources/output/monthly_assets.csv")

apptech = all_assets[all_assets['Symbol'] == 'APCX']
Buzzfeed = all_assets[all_assets['Symbol'] == 'ENFA']

buzz_report = Buzzfeed.withColumn('Intraday_Delta', Buzzfeed['Adj Close'] - Buzzfeed['Open'])
apptech_report = apptech.withColumn('Intraday_Delta', apptech['Adj Close'] - apptech['Open'])

kept_values = ['Date', 'Open', 'Adj Close', 'Intraday_Delta']

final_report_buzzfeed = buzz_report[kept_values]
final_report_apptech = apptech_report[kept_values]

final_report_buzzfeed.write.mode('overwrite').csv("../datasources/report/buzzfeed.csv")
final_report_apptech.write.mode('overwrite').csv("../datasources/report/AppTech.csv")

# Stop the Spark session after having sent the metadata
time.sleep(30)
spark.stop()