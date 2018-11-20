#For Python, you can use the --py-files argument of spark-submit to add .py, .zip or .egg files to be distributed with your application. If you depend on multiple Python files we recommend packaging them into a .zip or .egg.
spark-submit --deploy-mode cluster --conf spark.yarn.maxAppAttempts=1 --conf spark.dynamicAllocation.enabled=true --conf spark.driver.maxResultSize=0 /mnt/grab_test_code/spark_process.py $1 $2 &

#PID=$! #catch the last PID, here from the above command
#echo "PID of the spark-submit job:$PID"
#wait $PID #wait for the above command to complete

exit_status=$?
echo "The exit status of the spark process was $exit_status"

if [ $exit_status -eq 0 ]; then
  echo "deleting the hdfs dir $1"
  hdfs dfs -rm -r $1
  echo "deleting the hdfs dir $2"
  hdfs dfs -rm -r $2
  exit
fi

exit
