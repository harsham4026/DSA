package com.intuit.blink.replicator.reconciler

import org.apache.spark.streaming._
import org.apache.spark.streaming.StreamingContext._
import org.apache.kafka.clients.consumer.ConsumerRecord
import org.apache.kafka.common.serialization.StringDeserializer
import org.apache.spark.streaming.kafka010._
import org.apache.spark.streaming.kafka010.LocationStrategies.PreferConsistent
import org.apache.spark.streaming.kafka010.ConsumerStrategies.Subscribe
import ch.hsr.geohash.GeoHash
import org.apache.spark.sql.functions._
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.types._
import java.util.Date
import java.text._
import harsha.grab_spark_streaming.TrafficCongestionCalculator


object SparkStreaming {

  val bootStapServer = "13.233.134.2:9092"
  val streamingIntervaal = 600
  val microBatchInterval = 10

  def main(args: Array[String]) {
    val spark = SparkSession.builder.appName("grab taxi data").getOrCreate()

    spark.conf.set("spark.sql.crossJoin.enabled", true)
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

    //    def twoPointsOnSameSide(x1 : Double, y1 : Double, x2 : Double, y2 : Double, px : Double, py : Double, qx : Double, qy : Double) : Boolean =  {
    //      var m =0.0;
    //      if (x1 == x2) {
    //        // vetical line
    //        if ((px < x1 && qx < x1) || (px > x1 && qx > x1))
    //          return true;
    //        else
    //          return false;
    //      } else {
    //        m = (y2 - y1) / (x2 - x1);
    //      }
    //      var c : Double = y1 - m * x1;
    //      val valp : Double = py - m * px - c;
    //      val valq : Double= qy - m * qx - c;
    //      if (valp * valq > 0) {
    //        return true;
    //      } else
    //        return false;
    //    }
    //
    //    def isIntersecting(x1 : Double,y1 : Double,x2 : Double,y2 : Double,x3 : Double,y3 : Double,x4 : Double, y4 : Double) :  Boolean = {
    //      // Considering line 1 x1 y1 x2 y2
    //      val case1 = twoPointsOnSameSide(x1, y1, x2, y2, x3, y3, x4, y4);
    //      // consider line 2 x3y3 x4y4
    //      val case2 = twoPointsOnSameSide(x3, y3, x4, y4, x1, y1, x2, y2);
    //      if (case1 == false && case2 == false) {
    //        //
    //        return true;
    //      }
    //      return false;
    //    }
    //
    //    def calculateCongestion = udf { (pickLat : Double, pickLong : Double, dropLat : Double, dropLong : Double, minLat : Double, minLong : Double, maxLat : Double, maxLong : Double, speed : Double)=>
    //      var congest = 0 ;
    //      if(isIntersecting(pickLat, pickLong, dropLat, dropLong,minLat, minLong, maxLat, minLong) ||
    //        isIntersecting(pickLat, pickLong, dropLat, dropLong ,maxLat, minLong, maxLat, maxLong) ||
    //        isIntersecting(pickLat, pickLong, dropLat, dropLong ,maxLat, maxLong, minLat, maxLong) ||
    //        isIntersecting(pickLat, pickLong, dropLat, dropLong ,minLat, minLong, minLat, maxLong) )
    //      {
    //        //Yes it crosses
    //        if(speed > speedThreshold) {
    //          congest=1;
    //        }
    //        else {
    //          congest= congest - 1;
    //        }
    //      }
    //      congest;
    //    }

    val ssc = new StreamingContext(spark.sparkContext, Seconds(microBatchInterval))


    val kafkaParamsUser = Map[String, Object](
      "bootstrap.servers" -> bootStapServer,
      "key.deserializer" -> classOf[StringDeserializer],
      "value.deserializer" -> classOf[StringDeserializer],
      "group.id" -> "user_group",
      "auto.offset.reset" -> "latest",
      "enable.auto.commit" -> (false: java.lang.Boolean)
    )

    val userTopic = Array("user")
    val userStream = KafkaUtils.createDirectStream[String, String](
      ssc,
      PreferConsistent,
      Subscribe[String, String](userTopic, kafkaParamsUser)
    )

    val kafkaParamsDriver = Map[String, Object](
      "bootstrap.servers" -> bootStapServer,
      "key.deserializer" -> classOf[StringDeserializer],
      "value.deserializer" -> classOf[StringDeserializer],
      "group.id" -> "driver_group",
      "auto.offset.reset" -> "latest",
      "enable.auto.commit" -> (false: java.lang.Boolean)
    )

    val driverTopic = Array("driver")
    val driverStream = KafkaUtils.createDirectStream[String, String](
      ssc,
      PreferConsistent,
      Subscribe[String, String](driverTopic, kafkaParamsDriver)
    )

    val kafkaParamsWeather = Map[String, Object](
      "bootstrap.servers" -> bootStapServer,
      "key.deserializer" -> classOf[StringDeserializer],
      "value.deserializer" -> classOf[StringDeserializer],
      "group.id" -> "weather_group",
      "auto.offset.reset" -> "latest",
      "enable.auto.commit" -> (false: java.lang.Boolean)
    )

    val weatherTopic = Array("weather")
    val weatherStream = KafkaUtils.createDirectStream[String, String](
      ssc,
      PreferConsistent,
      Subscribe[String, String](weatherTopic, kafkaParamsWeather)
    )

    val kafkaParamsTrips = Map[String, Object](
      "bootstrap.servers" -> bootStapServer,
      "key.deserializer" -> classOf[StringDeserializer],
      "value.deserializer" -> classOf[StringDeserializer],
      "group.id" -> "trips_group",
      "auto.offset.reset" -> "latest",
      "enable.auto.commit" -> (false: java.lang.Boolean)
    )

    val tripsTopic = Array("tripdata")
    val tripRDDStream = KafkaUtils.createDirectStream[String, String](
      ssc,
      PreferConsistent,
      Subscribe[String, String](tripsTopic, kafkaParamsTrips)
    )

    val streamedDataUser = userStream.map(record => record.value).map(record => record.split(",")).map(record => (GeoHash.geoHashStringWithCharacterPrecision(record(0).toDouble, record(1).toDouble, 6), 1))
    val uw = streamedDataUser.reduceByKeyAndWindow((a: Int, b: Int) => (a + b), Seconds(streamingIntervaal), Seconds(streamingIntervaal))

    val streamedDataDriver = driverStream.map(record => record.value).map(record => record.split(",")).map(record => (GeoHash.geoHashStringWithCharacterPrecision(record(0).toDouble, record(1).toDouble, 6), 1))
    val dw = streamedDataDriver.reduceByKeyAndWindow((a: Int, b: Int) => (a + b), Seconds(streamingIntervaal), Seconds(streamingIntervaal))

    val streamedDataWeather = weatherStream.map(record => record.value).map(record => record.split(",")).map(record => (record(0), record(1), record(2))).window(Seconds(streamingIntervaal), Seconds(streamingIntervaal))

    val tripsDataStream = tripRDDStream.map(record => record.value).map(record => record.split(",")).map(record => (record(0), record(1), record(2), record(3), record(4))).window(Seconds(streamingIntervaal), Seconds(streamingIntervaal))

    val supplyDemandStream = dw.join(uw).map(x => (x._1, x._2._1.toDouble / x._2._2.toDouble)).foreachRDD { rdd =>
      import spark.implicits._
      val supplyDemandDataFrame = spark.createDataFrame(rdd).toDF("geo_hash", "supply_demand_ratio")
      supplyDemandDataFrame.write.format("parquet").mode("overwrite").save("s3a://grab-test-data/supply_demand_ratio/")
      supplyDemandDataFrame.show()
    }

    val congestionDataStream = tripsDataStream.foreachRDD { rdd =>
      import spark.implicits._
      val currentDate = dateFormatter.format(new Date())
      val tripDF = spark.createDataFrame(rdd).toDF("pickLat", "pickLong", "dropLat", "dropLong", "speed")
      val congDF = tripDF.join(zonesDFBroadcast.value).withColumn("congest", TrafficCongestionCalculator.calculateCongestion(
        col("pickLat"), col("pickLong"), col("dropLat"), col("dropLong"), col("minLat"), col("minLong"), col("maxLat"), col("maxLong"), col("speed")))
      val finalDF = congDF.groupBy(col("geohash")).agg(sum(col("congest")).alias("congest")).select(col("geohash").cast("string"), col("congest").cast("int"))
      finalDF.show()
      finalDF.write.format("parquet").mode("overwrite").save("s3a://grab-test-data/congestion_data_streaming/")
      finalDF.withColumn("time_stamp", lit(unix_timestamp())).write.format("parquet").mode("append").save("s3a://grab-test-data/congestion_data_batch/" + currentDate + "/")
    }

    streamedDataWeather.foreachRDD { rdd =>
      import spark.implicits._
      val weatherStreamDataFrame = spark.createDataFrame(rdd).toDF("geo_hash", "temparature", "precipitation")
      weatherStreamDataFrame.select(col("geo_hash"), col("temparature").cast("double"), col("precipitation").cast("double")).withColumn("time_stamp", lit(unix_timestamp())).write.format("parquet").mode("overwrite").save("s3a://grab-test-data/weather_data_streaming/")
      weatherStreamDataFrame.show()
    }

    uw.foreachRDD { rdd =>
      import spark.implicits._
      val currentDate = dateFormatter.format(new Date())
      val userStreamDataFrame = spark.createDataFrame(rdd).toDF("geo_hash", "count")
      userStreamDataFrame.withColumn("time_stamp", lit(unix_timestamp())).write.format("parquet").mode("append").save("s3a://grab-test-data/user_data/" + currentDate + "/")
      userStreamDataFrame.show()
    }

    dw.foreachRDD { rdd =>
      import spark.implicits._
      val currentDate = dateFormatter.format(new Date())
      val driverStreamDataFrame = spark.createDataFrame(rdd).toDF("geo_hash", "count")
      driverStreamDataFrame.withColumn("time_stamp", lit(unix_timestamp())).write.format("parquet").mode("append").save("s3a://grab-test-data/driver_data/" + currentDate + "/")
      driverStreamDataFrame.show()
    }

    streamedDataWeather.foreachRDD { rdd =>
      import spark.implicits._
      val currentDate = dateFormatter.format(new Date())
      val weatherStreamDataFrame = spark.createDataFrame(rdd).toDF("geo_hash", "temparature", "precipitation")
      weatherStreamDataFrame.select(col("geo_hash"), col("temparature").cast("double"), col("precipitation").cast("double")).withColumn("time_stamp", lit(unix_timestamp())).write.format("parquet").mode("append").save("s3a://grab-test-data/weather_data_batch/" + currentDate + "/")
      weatherStreamDataFrame.show()
    }

    ssc.start()
    ssc.awaitTermination()
  }

}
