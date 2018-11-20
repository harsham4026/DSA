//spark-shell --jars spark-streaming-kafka-0-10-assembly_2.11-2.3.0.jar,geohash-1.2.0.jar

import org.apache.spark.streaming._
import org.apache.spark.streaming.StreamingContext._
import org.apache.kafka.clients.consumer.ConsumerRecord
import org.apache.kafka.common.serialization.StringDeserializer
import org.apache.spark.streaming.kafka010._
import org.apache.spark.streaming.kafka010.LocationStrategies.PreferConsistent
import org.apache.spark.streaming.kafka010.ConsumerStrategies.Subscribe
import ch.hsr.geohash.GeoHash
import org.apache.spark.sql.functions._

val ssc = new StreamingContext(sc, Seconds(10))


val kafkaParamsUser = Map[String, Object](
  "bootstrap.servers" -> "13.233.134.2:9092",
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
  "bootstrap.servers" -> "13.233.134.2:9092",
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
  "bootstrap.servers" -> "13.233.134.2:9092",
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

val streamedDataUser = userStream.map(record => record.value).map(record => record.split(",")).map(record => (GeoHash.geoHashStringWithCharacterPrecision(record(0).toDouble, record(1).toDouble, 6), 1) )

val streamedDataDriver = driverStream.map(record => record.value).map(record => record.split(",")).map(record => (GeoHash.geoHashStringWithCharacterPrecision(record(0).toDouble, record(1).toDouble, 6), 1) )

//val streamedDataWeather = weatherStream.map(record => record.value).map(record => record.split(",")).map(record => (record(0), record(1) ))

val uw = streamedDataUser.reduceByKeyAndWindow((a:Int, b:Int) => (a + b), Seconds(120), Seconds(120))

val dw = streamedDataDriver.reduceByKeyAndWindow((a:Int, b:Int) => (a + b), Seconds(120), Seconds(120))

val supplyDemandStream = dw.join(uw).map(x => (x._1, x._2._1.toDouble/x._2._2.toDouble)).foreachRDD { rdd=>
          import spark.implicits._
          val supplyDemandDataFrame = spark.createDataFrame(rdd).toDF("geo_hash", "supply_demand_ratio")
          supplyDemandDataFrame.write.format("parquet").mode("overwrite").save("s3a://grab-test-data/supply_demand_ratio/")
          supplyDemandDataFrame.show()
        }

uw.foreachRDD { rdd=>
      import spark.implicits._
      val wordsDataFrame = spark.createDataFrame(rdd).toDF("geo_hash", "count")
      wordsDataFrame.withColumn("time_stamp", lit(current_timestamp())).write.format("parquet").mode("append").save("s3a://grab-test-data/user_data/")
      wordsDataFrame.show()
    }
dw.foreachRDD { rdd=>
          import spark.implicits._
          val wordsDataFrame = spark.createDataFrame(rdd).toDF("geo_hash", "count")
          wordsDataFrame.withColumn("time_stamp", lit(current_timestamp())).write.format("parquet").mode("append").save("s3a://grab-test-data/driver_data/")
          wordsDataFrame.show()
        }

ssc.start()
ssc.awaitTermination()







scala> val rdd = sc.parallelize(Array("1,2,3", "4,5,6", "7,8,9", "10,11,12")).map(_.split(",")).map(x => (x(0), x(1) ))
rdd: org.apache.spark.rdd.RDD[(String, String)] = MapPartitionsRDD[18] at map at <console>:24

scala> val rdd1 = sc.parallelize(Array("1,2,3", "4,5,6", "7,8,9", "10,11,12")).map(_.split(",")).map(x => (x(0), x(1) ))
rdd1: org.apache.spark.rdd.RDD[(String, String)] = MapPartitionsRDD[21] at map at <console>:24

scala> val rdd2 = sc.parallelize(Array("1,2,3", "4,5,6", "7,8,9", "10,11,12")).map(_.split(",")).map(x => (x(0), x(1) ))
rdd2: org.apache.spark.rdd.RDD[(String, String)] = MapPartitionsRDD[24] at map at <console>:24

scala> rdd.join(rdd1).join(rdd2)
res1: org.apache.spark.rdd.RDD[(String, ((String, String), String))] = MapPartitionsRDD[30] at join at <console>:30

scala> rdd.join(rdd1).join(rdd2).map(x => (x._1, x._2._1._1, x._2._1._2, x._2._2)).take(1)
res6: Array[(String, String, String, String)] = Array((1,2,2,2))
