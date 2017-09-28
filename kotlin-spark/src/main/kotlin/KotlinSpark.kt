import org.apache.spark.SparkConf
import org.apache.spark.api.java.JavaSparkContext
import kotlin.reflect.KClass



fun main( args : Array<String> ) {
  val largs = args.toList() 
  val conf = SparkConf()
          .setMaster("local")
          .setAppName("Kotlin Spark Test")
  val sc = JavaSparkContext(conf)
  println("Initialized Kotlin Spark.") 
  println("Args = ${largs}")
  when { 
    largs.contains("textSumUp") -> textSumUp(sc)
    largs.contains("commerceStats") -> CommerceStats.main(sc)
  }
}
