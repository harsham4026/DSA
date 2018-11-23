#!/usr/bin/env bash
spark-submit --class harsha.grab_spark_streaming.SparkStreaming --master yarn --deploy-mode cluster --conf spark.dynamicAllocation.enabled=true grab_spark_streaming-1.0-SNAPSHOT.jar /home/hadoop/grab_data_processing.properties
