# pip install --user kafka-python

from kafka import KafkaConsumer
#import pygeohash
#from pyspark.sql.functions import udf
#from pyspark.sql.types import StringType
#from pyspark.sql import functions as F
from pyspark.sql import SparkSession
import datetime
import time
from datetime import timedelta
import subprocess

user_messages_staging = "hdfs:///grab_data/user_messages_staging/"
driver_messages_staging = "hdfs:///grab_data/driver_messages_staging/"
spark_script_path= '/mnt/grab_test_code/py_spark_submit_script.sh'

input_schema = ["lat", "long", "timestamp"]

#calcualte_the_geohash_udf = udf(lambda x, y: pygeohash.encode(float(x), float(y)), StringType())

consumerUser = KafkaConsumer('user', group_id='my-group', bootstrap_servers=['13.233.134.2:9092'])
consumerDriver = KafkaConsumer('driver', group_id='my-group2', bootstrap_servers=['13.233.134.2:9092'])

spark = SparkSession.builder.appName('supply-to-demand-app').getOrCreate()

while True:
    start_time = time.time()
    userMsgsValues = []
    driverMsgsValues = []
    userMsgs = consumerUser.poll(1000, 100)
    driverMsgs = consumerDriver.poll(1000, 100)

    for msg in userMsgs:
        for value in userMsgs[msg]:
            userMsgsValues.append(value[6].split(','))

    for msg in driverMsgs:
        for value in driverMsgs[msg]:
            driverMsgsValues.append(value[6].split(','))

    # CALL THE SPARK PROCESS TO CONVERT TO SUPPLY DEMAND AND SAVE TO HDFS
    current_time = datetime.datetime.today().strftime('%Y_%m_%d_%H_%M')

    user_messages_hdfs_path = user_messages_staging + current_time
    driver_messages_hdfs_path = driver_messages_staging + current_time

    # convert the two lists to dataframes and need to run this spark in a separate subprocess
    driver_msgs_df = spark.createDataFrame(driverMsgsValues, input_schema).write.format('parquet').mode('append').save(driver_messages_hdfs_path)
    user_msgs_df = spark.createDataFrame(userMsgsValues, input_schema).write.format('parquet').mode('append').save(user_messages_hdfs_path)

    #invoking spark using child process and don't wait on it
    subprocess.Popen(['sh', spark_script_path, driver_messages_hdfs_path, user_messages_hdfs_path], shell=True,stdin=None,stdout=None,stderr=None,close_fds=True)

    # write to hdfs then suvprocess trigger the spark supply demand and count
    end_time = time.time()
    #write the driver_msgs_df and user_msgs_df to hdfs copy to s3 and create athena table on top of it for visualization
    time.sleep(600 - int(timedelta(seconds=end_time - start_time).total_seconds()))
