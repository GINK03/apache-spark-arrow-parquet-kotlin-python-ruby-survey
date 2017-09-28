import org.apache.spark.SparkConf
import org.apache.spark.api.java.JavaSparkContext
import kotlin.reflect.KClass

import java.nio.file.Files
import java.io.*
import java.lang.*
import com.google.gson.Gson
import com.google.gson.reflect.TypeToken


typealias Data = Map<String, Any>
data class CS(val contory:String, val city:String, val Y1974:Double?, val Y1976:Double?, val Y1979:Double?, val Y1982:Double?, val Y1985:Double?, val Y1988:Double?, val Y1991:Double?, val Y1994:Double?, val Y1997:Double?, val Y2002:Double?, val Y2004:Double?, val Y2007:Double? )
object CommerceStats {
  val gson = Gson()
  val Type = object : TypeToken<Data>() {}.type
  fun load() : List<Data> {
    println("aaaaaaaa") 
    val df = File("../resource/商業統計.json")
      .readText()
      .toString()
      .split("\n")
      .map { 
        val data:Data?  = gson.fromJson<Data>(it, Type)
        data
      }.filter { 
        it != null
      }.map { it!! }
    return df
  }
  fun main(sc : JavaSparkContext) {
    val css = load()
    val input = sc.parallelize(css)
    val ans = input.groupBy {
      it["contory"]
    }.map {
      val (key, vals) = Pair( it._1(), it._2() )// println( it )
      val size = vals.toList().size
      val total = vals.map { 
        val size = it.toList().size
        val sum = it.toList().filter {
          it.first.matches(Regex("Y[0-9]+"))
        }.map { 
          try { it.second.toString().toDouble() } catch (e: java.lang.Exception ) { 0.0 } 
        }.reduce { y,x -> y + x }
        sum/size
      }.reduce { y, x -> y + x }
      Pair(key, total/size)
    }.collect()
    ans.sortedBy {
      it.second * -1
    }.map {
      println(it)
    }
  }
}

