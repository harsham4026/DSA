package harsha.grab_spark_streaming


import java.net.URI
import java.text._
import java.util._

import org.apache.hadoop.conf.Configuration
import org.apache.hadoop.fs.{FileStatus, FileSystem, Path}
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._

object SparkBatchProcess {

  var datesList = new ArrayList[String]
  val fsScheme = "s3://grab-test-data"
  val spark = SparkSession.builder.appName("grab taxi data day aggregation").getOrCreate()
  val conf = new Configuration();
  val fs = FileSystem.get(new URI("s3://grab-test-data"), conf)
  val dateFormatter = new SimpleDateFormat("yyyy_MM_dd")
  var currentDate = dateFormatter.format(new Date())
  //val currentDate = dateFormatter.format(new Date())
  //DATE=`date +%Y_%m_%d`
  val dataOfDaysToHold = 5

  def main(args: Array[String]): Unit = {

    currentDate = args(0)

    val weatherData = spark.read.parquet("s3a://grab-test-data/weather_data_batch/" + currentDate + "/").select(col("geo_hash"), col("temparature"), col("precipitation"), from_unixtime(col("time_stamp"), "yyyy-MM-dd HH").as("time_stamp")).groupBy("geo_hash", "time_stamp").agg(sum("temparature").as("temparature"), sum("precipitation").as("precipitation"))

    val driverData = spark.read.parquet("s3a://grab-test-data/driver_data/" + currentDate + "/").select(col("geo_hash"), col("count"), from_unixtime(col("time_stamp"), "yyyy-MM-dd HH").as("time_stamp")).groupBy("geo_hash", "time_stamp").agg(sum("count").as("supplyCount"))

    val userData = spark.read.parquet("s3a://grab-test-data/user_data/" + currentDate + "/").select(col("geo_hash"), col("count"), from_unixtime(col("time_stamp"), "yyyy-MM-dd HH").as("time_stamp")).groupBy("geo_hash", "time_stamp").agg(sum("count").as("demandCount"))

    val congestionData = spark.read.parquet("s3a://grab-test-data/congestion_data_batch/" + currentDate + "/").select(col("geohash").as("geo_hash"), col("congest"), col("time_stamp")).select(col("geo_hash"), col("congest"), from_unixtime(col("time_stamp"), "yyyy-MM-dd HH").as("time_stamp")).groupBy("geo_hash", "time_stamp").agg(sum("congest").as("congest"))


    val groupedHourlyData = congestionData.join(weatherData, Seq("geo_hash", "time_stamp")).join(userData, Seq("geo_hash", "time_stamp"), "left_outer").join(driverData, Seq("geo_hash", "time_stamp"), "left_outer").na.fill(0)

    groupedHourlyData.write.format("parquet").mode("append").save("s3a://grab-test-data/hourly_data_aggregation/")

    var userFileStatus = fs.listStatus(new Path("s3://grab-test-data/user_data"))
    var driverFileStatus = fs.listStatus(new Path("s3://grab-test-data/driver_data"))
    var weatherDataFileStatus = fs.listStatus(new Path("s3://grab-test-data/weather_data_batch"))
    var congestionDataFileStatus = fs.listStatus(new Path("s3://grab-test-data/congestion_data_batch"))

    getTheOlderDaysInList()

    deleteTheFoldersOlderThanThreshold(userFileStatus)
    deleteTheFoldersOlderThanThreshold(driverFileStatus)
    deleteTheFoldersOlderThanThreshold(weatherDataFileStatus)
    deleteTheFoldersOlderThanThreshold(congestionDataFileStatus)

  }

  def getTheOlderDaysInList() = {
    val input = currentDate;
    val myDate = dateFormatter.parse(input);
    for (day <- 1 to dataOfDaysToHold) {
      val cal1 = Calendar.getInstance();
      cal1.setTime(myDate);
      cal1.add(Calendar.DAY_OF_YEAR, -day);
      datesList.add(dateFormatter.format(cal1.getTime()))
    }
  }

  def deleteTheFoldersOlderThanThreshold(fileStatus: Array[FileStatus]): Unit = {
    for (status <- fileStatus) {
      if (datesList.contains(status.getPath().toString().split("/")(4))) {
      }
      else {
        //status.getPath.getName
        fs.delete(status.getPath(), true)
      }
    }
  }

}
