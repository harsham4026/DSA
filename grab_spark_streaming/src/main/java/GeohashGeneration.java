package com.intuit.blink.foreman.manager;

import ch.hsr.geohash.GeoHash;

import java.io.*;
import java.util.HashMap;
import java.util.Map;
import java.util.Set;

public class GeohashGeneration {

  public static void main(String[] args) throws FileNotFoundException, IOException {
    double latEnd = 40.73849587;//
    double longEnd = -74.16120799;

    Map<String, String> geoHashMap = new HashMap<>();

    for (double latStart = 40.68951565; latStart < latEnd; latStart = latStart + 0.00001) {
      for (double longStart = -74.17678575; longStart < longEnd; longStart = longStart + 0.00001) {

        //List<String> latLongSet = new ArrayList<>();
        //latLongSet.add(Double.toString(latStart) + "," + Double.toString(latEnd));
        geoHashMap.put(GeoHash.geoHashStringWithCharacterPrecision(latStart, longStart, 6), "");
        //multiMap.put(GeoHash.geoHashStringWithCharacterPrecision(latStart, latEnd, 6), Double.toString(latStart) + "," + Double.toString(latEnd));
      }

    }

    Set<String> keys = geoHashMap.keySet();
    System.out.println("size of keys " + keys.size());
    File fout = new File("/Users/hmandadi/Desktop/working/long_modified_0_0001.txt");
    FileOutputStream fos = new FileOutputStream(fout);
    BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(fos));

    for (String key : keys) {
      bw.write(key);
      bw.newLine();
      System.out.println(key);
      //System.out.println("geo_hash_list = " + multiMap.get(key) + "n");
    }

  }
}
