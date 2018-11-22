package harsha.grab_spark_streaming

import org.apache.spark.sql.functions.udf

object TrafficCongestionCalculator {

  val speedThreshold = 30.0

  def calculateCongestion = udf { (pickLat: Double, pickLong: Double, dropLat: Double, dropLong: Double, minLat: Double, minLong: Double, maxLat: Double, maxLong: Double, speed: Double) =>
    var congest = 0;
    if (isIntersecting(pickLat, pickLong, dropLat, dropLong, minLat, minLong, maxLat, minLong) ||
      isIntersecting(pickLat, pickLong, dropLat, dropLong, maxLat, minLong, maxLat, maxLong) ||
      isIntersecting(pickLat, pickLong, dropLat, dropLong, maxLat, maxLong, minLat, maxLong) ||
      isIntersecting(pickLat, pickLong, dropLat, dropLong, minLat, minLong, minLat, maxLong)) {
      //Yes it crosses
      if (speed > speedThreshold) {
        congest = 1;
      }
      else {
        congest = congest - 1;
      }
    }
    congest;
  }

  def isIntersecting(x1: Double, y1: Double, x2: Double, y2: Double, x3: Double, y3: Double, x4: Double, y4: Double): Boolean = {
    // Considering line 1 x1 y1 x2 y2
    val case1 = twoPointsOnSameSide(x1, y1, x2, y2, x3, y3, x4, y4);
    // consider line 2 x3y3 x4y4
    val case2 = twoPointsOnSameSide(x3, y3, x4, y4, x1, y1, x2, y2);
    if (case1 == false && case2 == false) {
      //
      return true;
    }
    return false;
  }

  def twoPointsOnSameSide(x1: Double, y1: Double, x2: Double, y2: Double, px: Double, py: Double, qx: Double, qy: Double): Boolean = {
    var m = 0.0;
    if (x1 == x2) {
      // vetical line
      if ((px < x1 && qx < x1) || (px > x1 && qx > x1))
        return true;
      else
        return false;
    } else {
      m = (y2 - y1) / (x2 - x1);
    }
    var c: Double = y1 - m * x1;
    val valp: Double = py - m * px - c;
    val valq: Double = qy - m * qx - c;
    if (valp * valq > 0) {
      return true;
    } else
      return false;
  }
}
