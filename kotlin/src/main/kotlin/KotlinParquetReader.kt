import org.apache.avro.generic.GenericRecord
import java.lang.Exception
import com.google.gson.Gson
import com.google.gson.reflect.TypeToken

typealias AnyData = List<Map<String,Any>>
typealias Hints = List<Map<String, Any>>


object Reader {
  fun memory(path:String) : Pair<AnyData, Hints> {
    val reader = JavaParquetUtils.getAvroParquetReaderInstance(path)
    val buff = mutableListOf<GenericRecord>()
    val gson = Gson()
    val type = object : TypeToken<Map<String, Any>>() {}.type
    val typeSchema = object : TypeToken<Map<String, Any>>() {}.type
    val res = mutableListOf<Map<String,Any>>()
    var hint:Hints? = null 
    scan@while(true) {
      val record = reader.read()
      if(record == null) break@scan
      buff.add( record )
      val json = record.toString()
      val map:Map<String,Any> = gson.fromJson<Map<String, Any>>(record.toString(), type)
      val types = gson.fromJson<Map<String, Any>>( record.getSchema().toString(), typeSchema )["fields"]
      val detail = types as List<Map<String, Any>>
      if( hint == null ) hint = detail
      res.add( map )
    }
    return Pair(res.toList() as AnyData, hint!! as Hints)
  }
}
