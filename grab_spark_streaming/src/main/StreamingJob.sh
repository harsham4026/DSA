#!/usr/bin/env bash
spark-submit --class harsha.grab_spark_streaming.SparkStreaming --master yarn --deploy-mode cluster --conf spark.dynamicAllocation.enabled=true grab_spark_streaming-1.0-SNAPSHOT.jar /home/hadoop/grab_data_processing.properties

#spark-submit --class harsha.grab_spark_streaming.SparkStreaming --master yarn --deploy-mode client --num-executors 2 --executor-cores 2 --executor-memory 5g --driver-memory 2g --driver-cores 1 grab_spark_streaming-1.0-SNAPSHOT.jar /home/hadoop/grab_data_processing.properties
