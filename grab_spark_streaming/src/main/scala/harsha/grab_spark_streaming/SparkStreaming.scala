package harsha.grab_spark_streaming

import java.io.FileInputStream
import java.net.URI
import java.text._
import java.util.{Date, Properties}

import ch.hsr.geohash.GeoHash
import org.apache.hadoop.conf.Configuration
import org.apache.hadoop.fs.{FileSystem, Path}
import org.apache.kafka.common.serialization.StringDeserializer
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._
import org.apache.spark.sql.types._
import org.apache.spark.streaming._
import org.apache.spark.streaming.kafka010.ConsumerStrategies.Subscribe
import org.apache.spark.streaming.kafka010.LocationStrategies.PreferConsistent
import org.apache.spark.streaming.kafka010._

object SparkStreaming {

  private val props = new Properties()

  def main(args: Array[String]) {
    val spark = SparkSession.builder.appName("grab taxi data streaming job").getOrCreate()
    val conf = new Configuration()
    val fs = FileSystem.get(new URI("s3://grab-test-data"), conf)

    props.load(fs.open(new Path(args(0))))

    //PropertiesConstants.loadTheProperties(props)

    val bootStrapServer = props.getProperty("bootstrap.server", "13.233.134.2:9092")

    val streamingInterval = (props.getProperty("streaming.interval", "600")).toInt
    val microBatchInterval = (props.getProperty("microbatch.interval", "10")).toInt
    val weatherStreamingInterval = (props.getProperty("weather.streaming.interval", "3600")).toInt

    val supplyDemandRatioStreamingPath = props.getProperty("streaming.supply.demand.ratio.path", "s3a://grab-test-data/supply_demand_ratio/")
    val congestionStreamingDataPath = props.getProperty("congestion.streaming.data", "s3a://grab-test-data/congestion_data_streaming/")

    val congestionBatchDataPath = props.getProperty("congestion.batch.data", "s3a://grab-test-data/congestion_data_batch/")
    val userBatchDataPath = props.getProperty("user.batch.data", "s3a://grab-test-data/user_data/")
    val driverBatchDataPath = props.getProperty("driver.batch.data", "s3a://grab-test-data/driver_data/")
    val weatherBatchDataPath = props.getProperty("weather.batch.data", "s3a://grab-test-data/weather_data_batch/")

    val userTopicName = props.getProperty("user.topic", "user")
    val driverTopicName = props.getProperty("driver.topic", "driver")
    val weatherTopicName = props.getProperty("weather.topic", "weather")
    val tripDataTopicName = props.getProperty("tripdata.topic", "tripdata")

    spark.conf.set("spark.sql.crossJoin.enabled", "true")
    spark.conf.set("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
    spark.conf.set("spark.broadcast.compress", "true")
    spark.conf.set("spark.shuffle.compress", "true")
    spark.conf.set("spark.shuffle.spill.compress", "true")
    spark.conf.set("spark.io.compression.codec", "org.apache.spark.io.LZ4CompressionCodec")
    spark.conf.set("spark.sql.inMemoryColumnarStorage.compressed", "true")
    spark.conf.set("spark.sql.autoBroadcastJoinThreshold", 52428800)

    val zonesSchema = StructType(Array(
      StructField("geohash", StringType, true),
      StructField("minLat", DoubleType, true),
      StructField("maxLat", DoubleType, true),
      StructField("minLong", DoubleType, true),
      StructField("maxLong", DoubleType, true)))

    val zoneDf = spark.read.format("csv").option("header", "true").option("mode", "DROPMALFORMED").schema(zonesSchema).load("s3a://grab-test-data/taxi_with_zones.csv")

    val zonesDFBroadcast = spark.sparkContext.broadcast(zoneDf) //zoneDf.persist()

    val dateFormatter = new SimpleDateFormat("yyyy_MM_dd")

    val ssc = new StreamingContext(spark.sparkContext, Seconds(microBatchInterval))


    val kafkaParamsUser = Map[String, Object](
      "bootstrap.servers" -> bootStrapServer,
      "key.deserializer" -> classOf[StringDeserializer],
      "value.deserializer" -> classOf[StringDeserializer],
      "group.id" -> "user_group",
      "auto.offset.reset" -> "latest",
      "enable.auto.commit" -> (false: java.lang.Boolean)
    )

    val userTopic = Array(userTopicName)
    val userStream = KafkaUtils.createDirectStream[String, String](
      ssc,
      PreferConsistent,
      Subscribe[String, String](userTopic, kafkaParamsUser)
    )

    val kafkaParamsDriver = Map[String, Object](
      "bootstrap.servers" -> bootStrapServer,
      "key.deserializer" -> classOf[StringDeserializer],
      "value.deserializer" -> classOf[StringDeserializer],
      "group.id" -> "driver_group",
      "auto.offset.reset" -> "latest",
      "enable.auto.commit" -> (false: java.lang.Boolean)
    )

    val driverTopic = Array(driverTopicName)
    val driverStream = KafkaUtils.createDirectStream[String, String](
      ssc,
      PreferConsistent,
      Subscribe[String, String](driverTopic, kafkaParamsDriver)
    )

    val kafkaParamsWeather = Map[String, Object](
      "bootstrap.servers" -> bootStrapServer,
      "key.deserializer" -> classOf[StringDeserializer],
      "value.deserializer" -> classOf[StringDeserializer],
      "group.id" -> "weather_group",
      "auto.offset.reset" -> "latest",
      "enable.auto.commit" -> (false: java.lang.Boolean)
    )

    val weatherTopic = Array(weatherTopicName)
    val weatherStream = KafkaUtils.createDirectStream[String, String](
      ssc,
      PreferConsistent,
      Subscribe[String, String](weatherTopic, kafkaParamsWeather)
    )

    val kafkaParamsTrips = Map[String, Object](
      "bootstrap.servers" -> bootStrapServer,
      "key.deserializer" -> classOf[StringDeserializer],
      "value.deserializer" -> classOf[StringDeserializer],
      "group.id" -> "trips_group",
      "auto.offset.reset" -> "latest",
      "enable.auto.commit" -> (false: java.lang.Boolean)
    )

    val tripsTopic = Array(tripDataTopicName)
    val tripRDDStream = KafkaUtils.createDirectStream[String, String](
      ssc,
      PreferConsistent,
      Subscribe[String, String](tripsTopic, kafkaParamsTrips)
    )

    val streamedDataUser = userStream.map(record => record.value).map(record => record.split(",")).map(record => (GeoHash.geoHashStringWithCharacterPrecision(record(0).toDouble, record(1).toDouble, 6), 1))
    val uw = streamedDataUser.reduceByKeyAndWindow((a: Int, b: Int) => (a + b), Seconds(streamingInterval), Seconds(streamingInterval))

    val streamedDataDriver = driverStream.map(record => record.value).map(record => record.split(",")).map(record => (GeoHash.geoHashStringWithCharacterPrecision(record(0).toDouble, record(1).toDouble, 6), 1))
    val dw = streamedDataDriver.reduceByKeyAndWindow((a: Int, b: Int) => (a + b), Seconds(streamingInterval), Seconds(streamingInterval))

    val streamedDataWeather = weatherStream.map(record => record.value).map(record => record.split(",")).map(record => (record(0), record(1), record(2))).window(Seconds(weatherStreamingInterval), Seconds(weatherStreamingInterval))

    val tripsDataStream = tripRDDStream.map(record => record.value).map(record => record.split(",")).map(record => (record(0), record(1), record(2), record(3), record(4))).window(Seconds(streamingInterval), Seconds(streamingInterval))

    val supplyDemandStream = dw.join(uw).map(x => (x._1, x._2._1.toDouble / x._2._2.toDouble)).foreachRDD { rdd =>

      val supplyDemandDataFrame = spark.createDataFrame(rdd).toDF("geo_hash", "supply_demand_ratio")
      supplyDemandDataFrame.write.format("parquet").mode("overwrite").save(supplyDemandRatioStreamingPath)
      supplyDemandDataFrame.show()
    }

    val congestionDataStream = tripsDataStream.foreachRDD { rdd =>

      val currentDate = dateFormatter.format(new Date())
      val tripDF = spark.createDataFrame(rdd).toDF("pickLat", "pickLong", "dropLat", "dropLong", "speed")
      val congDF = tripDF.join(zonesDFBroadcast.value).withColumn("congest", TrafficCongestionCalculator.calculateCongestion(
        col("pickLat"), col("pickLong"), col("dropLat"), col("dropLong"), col("minLat"), col("minLong"), col("maxLat"), col("maxLong"), col("speed")))
      val finalDF = congDF.groupBy(col("geohash")).agg(sum(col("congest")).alias("congest")).select(col("geohash").cast("string"), col("congest").cast("int"))
      finalDF.show()
      finalDF.write.format("parquet").mode("overwrite").save(congestionStreamingDataPath)
      finalDF.withColumn("time_stamp", lit(unix_timestamp())).write.format("parquet").mode("append").save(congestionBatchDataPath + currentDate + "/")
    }

    //    streamedDataWeather.foreachRDD { rdd =>
    //      import spark.implicits._
    //      val weatherStreamDataFrame = spark.createDataFrame(rdd).toDF("geo_hash", "temparature", "precipitation")
    //      weatherStreamDataFrame.select(col("geo_hash"), col("temparature").cast("double"), col("precipitation").cast("double")).withColumn("time_stamp", lit(unix_timestamp())).write.format("parquet").mode("overwrite").save("s3a://grab-test-data/weather_data_streaming/")
    //      weatherStreamDataFrame.show()
    //    }

    uw.foreachRDD { rdd =>

      val currentDate = dateFormatter.format(new Date())
      val userStreamDataFrame = spark.createDataFrame(rdd).toDF("geo_hash", "count")
      userStreamDataFrame.withColumn("time_stamp", lit(unix_timestamp())).write.format("parquet").mode("append").save(userBatchDataPath + currentDate + "/")
      userStreamDataFrame.show()
    }

    dw.foreachRDD { rdd =>

      val currentDate = dateFormatter.format(new Date())
      val driverStreamDataFrame = spark.createDataFrame(rdd).toDF("geo_hash", "count")
      driverStreamDataFrame.withColumn("time_stamp", lit(unix_timestamp())).write.format("parquet").mode("append").save(driverBatchDataPath + currentDate + "/")
      driverStreamDataFrame.show()
    }

    streamedDataWeather.foreachRDD { rdd =>

      val currentDate = dateFormatter.format(new Date())
      val weatherStreamDataFrame = spark.createDataFrame(rdd).toDF("geo_hash", "temparature", "precipitation")
      weatherStreamDataFrame.select(col("geo_hash"), col("temparature").cast("double"), col("precipitation").cast("double")).withColumn("time_stamp", lit(unix_timestamp())).write.format("parquet").mode("append").save(weatherBatchDataPath + currentDate + "/")
      weatherStreamDataFrame.show()
    }

    ssc.start()
    ssc.awaitTermination()
  }

}
