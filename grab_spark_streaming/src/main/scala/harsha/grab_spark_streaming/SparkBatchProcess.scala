package harsha.grab_spark_streaming


import java.io.FileInputStream
import java.net.URI
import java.text._
import java.util._

import org.apache.hadoop.conf.Configuration
import org.apache.hadoop.fs.{FileStatus, FileSystem, Path}
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._
import org.apache.spark.SparkFiles


object SparkBatchProcess {

  private val datesList = new ArrayList[String]
  private val dateFormatter = new SimpleDateFormat("yyyy_MM_dd")
  private var currentDate = dateFormatter.format(new Date())
  private var dataOfDaysToHold = 5

  val propsFilePath = "hdfs:///grab_data_processing.properties"

  def main(args: Array[String]): Unit = {
    val props = new Properties()

    currentDate = args(0)

    //var fsScheme = props.getProperty("fs.scheme", "s3://grab-test-data")

    val spark = SparkSession.builder.appName("grab taxi data batch job aggregation").getOrCreate()
    val conf = new Configuration()
    val fs = FileSystem.get(new URI("s3://grab-test-data"), conf)

    props.load(fs.open(new Path(args(1))))
    dataOfDaysToHold = (props.getProperty("days.of.data.tohold", "5")).toInt

    val weatherBatchData = props.getProperty("weather.batch.data", "s3a://grab-test-data/weather_data_batch/")
    val driverBatchData = props.getProperty("driver.batch.data", "s3a://grab-test-data/driver_data/")
    val userBatchData = props.getProperty("user.batch.data", "s3a://grab-test-data/user_data/")
    val congestionBatchData = props.getProperty("congestion.batch.data", "s3a://grab-test-data/congestion_data_batch/")
    val hourlyAggregatedData = props.getProperty("hourly.aggreagated.data.path", "s3a://grab-test-data/hourly_data_aggregation/")

    val userFileStatus = props.getProperty("user.file.status", "s3://grab-test-data/user_data")
    val driverFileStatus = props.getProperty("driver.file.status", "s3://grab-test-data/driver_data")
    val weatherFileStatus = props.getProperty("weather.data.file.status", "s3://grab-test-data/weather_data_batch")
    val congestionFileStatus = props.getProperty("congestion.data.file.status", "s3://grab-test-data/congestion_data_batch")

    val weatherData = spark.read.parquet(weatherBatchData + currentDate + "/").select(col("geo_hash"), col("temparature"), col("precipitation"), from_unixtime(col("time_stamp"), "yyyy-MM-dd HH").as("time_stamp")).groupBy("geo_hash", "time_stamp").agg(sum("temparature").as("temparature"), sum("precipitation").as("precipitation"))

    val driverData = spark.read.parquet(driverBatchData + currentDate + "/").select(col("geo_hash"), col("count"), from_unixtime(col("time_stamp"), "yyyy-MM-dd HH").as("time_stamp")).groupBy("geo_hash", "time_stamp").agg(sum("count").as("supplyCount"))

    val userData = spark.read.parquet(userBatchData + currentDate + "/").select(col("geo_hash"), col("count"), from_unixtime(col("time_stamp"), "yyyy-MM-dd HH").as("time_stamp")).groupBy("geo_hash", "time_stamp").agg(sum("count").as("demandCount"))

    val congestionData = spark.read.parquet(congestionBatchData + currentDate + "/").select(col("geohash").as("geo_hash"), col("congest"), col("time_stamp")).select(col("geo_hash"), col("congest"), from_unixtime(col("time_stamp"), "yyyy-MM-dd HH").as("time_stamp")).groupBy("geo_hash", "time_stamp").agg(sum("congest").as("congest"))


    val groupedHourlyData = congestionData.join(weatherData, Seq("geo_hash", "time_stamp")).join(userData, Seq("geo_hash", "time_stamp"), "left_outer").join(driverData, Seq("geo_hash", "time_stamp"), "left_outer").na.fill(0)

    groupedHourlyData.write.format("parquet").mode("append").save(hourlyAggregatedData)

    var userFileStatusPath = fs.listStatus(new Path(userFileStatus))
    var driverFileStatusPath = fs.listStatus(new Path(driverFileStatus))
    var weatherDataFileStatusPath = fs.listStatus(new Path(weatherFileStatus))
    var congestionDataFileStatusPath = fs.listStatus(new Path(congestionFileStatus))

    getTheOlderDaysInList()

    deleteTheFoldersOlderThanThreshold(userFileStatusPath, fs)
    deleteTheFoldersOlderThanThreshold(driverFileStatusPath, fs)
    deleteTheFoldersOlderThanThreshold(weatherDataFileStatusPath, fs)
    deleteTheFoldersOlderThanThreshold(congestionDataFileStatusPath, fs)

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

  def deleteTheFoldersOlderThanThreshold(fileStatus: Array[FileStatus], fs: FileSystem): Unit = {
    for (status <- fileStatus) {
      if (datesList.contains(status.getPath().getName())) {
      }
      else {
        fs.delete(status.getPath(), true)
      }
    }
  }
}
