#call from subprocess in kafka consumer part

import pygeohash
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType
from pyspark.sql import functions as F
from pyspark.sql import SparkSession
import sys

user_messages_for_batch_processing_hdfs_path = "hdfs:///grab_data/user_messages_for_batch_processing"
driver_messages_for_batch_processing_hdfs_path = "hdfs:///grab_data/driver_messages_for_batch_processing"
supply_to_demand_ratio_for_stream_processing_hdfs_path = "hdfs:///grab_data/supply_to_demand_ratio_for_stream_processing"

calcualte_the_geohash_udf = udf(lambda x, y: pygeohash.encode(float(x), float(y), precision=6), StringType())

spark = SparkSession.builder.appName('supply-to-demand-app').getOrCreate()

#'hdfs:///grab_data/user_values_staging/'

driver_messages_hdfs_path = sys.argv[1]
user_messages_hdfs_path = sys.argv[2]

driver_msgs_df = spark.read.parquet(driver_messages_hdfs_path).withColumn("geo_hash", calcualte_the_geohash_udf("lat","long")).select("geo_hash", F.col("timestamp").cast('timestamp').alias('time')).select("geo_hash", F.from_unixtime(F.unix_timestamp('time', 'yyyy-MM-dd HH:mm:ss'), 'yyyy-MM-dd HH:mm').alias('date_time')).groupBy("geo_hash", "date_time").agg(F.count("*").alias("supply_count"))
user_msgs_df = spark.read.parquet(user_messages_hdfs_path).withColumn("geo_hash", calcualte_the_geohash_udf("lat", "long")).select("geo_hash", F.col("timestamp").cast('timestamp').alias('time')).select("geo_hash", F.from_unixtime(F.unix_timestamp('time', 'yyyy-MM-dd HH:mm:ss'), 'yyyy-MM-dd HH:mm').alias('date_time')).groupBy("geo_hash", "date_time").agg(F.count("*").alias("demand_count"))


driver_msgs_df.write.format('parquet').mode('append').save(driver_messages_for_batch_processing_hdfs_path)
user_msgs_df.write.format('parquet').mode('append').save(user_messages_for_batch_processing_hdfs_path)

#supply_demand_ration_df = user_msgs_df.join(driver_msgs_df, (driver_msgs_df.geo_hash == user_msgs_df.geo_hash) & (driver_msgs_df.date_time == user_msgs_df.date_time)).withColumn("supply_demand_ratio", (driver_msgs_df.supply_count/user_msgs_df.demand_count)).select(driver_msgs_df.geo_hash, driver_msgs_df.date_time, "supply_demand_ratio")

supply_demand_ration_df = user_msgs_df.join( driver_msgs_df, driver_msgs_df.geo_hash == user_msgs_df.geo_hash ).withColumn("supply_demand_ratio", (driver_msgs_df.supply_count/user_msgs_df.demand_count)).select(driver_msgs_df.geo_hash, "supply_demand_ratio")

supply_demand_ration_df.write.format('parquet').mode('append').save(supply_to_demand_ratio_for_stream_processing_hdfs_path)
