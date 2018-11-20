//spark-shell --jars:spark-streaming-kafka-0-10-assembly_2.11-2.3.0.jar,geohash-1.2.0.jar

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
val user_stream = KafkaUtils.createDirectStream[String, String](
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
val driver_stream = KafkaUtils.createDirectStream[String, String](
  ssc,
  PreferConsistent,
  Subscribe[String, String](driverTopic, kafkaParamsDriver)
)

val streamed_data_user = user_stream.map(record => record.value).map(record => record.split(",")).map(record => (GeoHash.geoHashStringWithCharacterPrecision(record(0).toDouble, record(1).toDouble, 6), 1) )

val streamed_data_driver = driver_stream.map(record => record.value).map(record => record.split(",")).map(record => (GeoHash.geoHashStringWithCharacterPrecision(record(0).toDouble, record(1).toDouble, 6), 1) )

val uw = streamed_data_user.reduceByKeyAndWindow((a:Int, b:Int) => (a + b), Seconds(120), Seconds(120))

val dw = streamed_data_driver.reduceByKeyAndWindow((a:Int, b:Int) => (a + b), Seconds(120), Seconds(120))

val abc = dw.join(uw).map(x => (x._1, x._2._1.toDouble/x._2._2.toDouble)).foreachRDD { rdd=>
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
