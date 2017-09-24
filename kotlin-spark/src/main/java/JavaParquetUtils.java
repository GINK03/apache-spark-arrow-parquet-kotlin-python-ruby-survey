
import java.io.File;
import java.io.IOException;
import org.apache.hadoop.fs.Path;
import org.apache.avro.Schema;
import org.apache.avro.LogicalType;
import org.apache.avro.generic.GenericData;
import org.apache.avro.generic.GenericFixed;
import org.apache.avro.generic.GenericRecord;
import org.apache.avro.generic.GenericRecordBuilder;
import org.apache.avro.util.Utf8;
import org.apache.parquet.schema.MessageType;
import org.apache.parquet.avro.AvroParquetReader;
public class JavaParquetUtils {
  public static AvroParquetReader<GenericRecord> getAvroParquetReaderInstance(String path) {
    Path file = new Path(path);
    try {
      AvroParquetReader<GenericRecord> reader = new AvroParquetReader<GenericRecord>(file);
      return reader;
    } 
    catch( java.io.IOException e ) {
      System.out.println(e);
      return null;
    }
  }

  public static void testLoad() {
    Path file = new Path("../python/local.pq");
    //AvroParquetReader<GenericRecord> reader = new AvroParquetReader.<GenericRecord>builder(file).build();
    try{ 
      AvroParquetReader<GenericRecord> reader = new AvroParquetReader<GenericRecord>(file);
      GenericRecord nextRecord = reader.read();
      while(true) {
        nextRecord = reader.read();
        if( nextRecord == null ) break;
        System.out.println( nextRecord );
      }
    }
    catch( java.io.IOException e ) {
      System.out.println(e);
    }
  }
}
