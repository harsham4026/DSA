#!/usr/bin/env bash
current_date=`date +%Y_%m_%d`
spark-submit --class harsha.grab_spark_streaming.SparkBatchProcess --master yarn --deploy-mode cluster --conf spark.dynamicAllocation.enabled=true grab_spark_streaming-1.0-SNAPSHOT.jar ${current_date} /home/hadoop/grab_data_processing.properties
