require "arrow"

Arrow::MemoryMappedInputStream.open("/tmp/file.arrow") do |input|
  reader = Arrow::RecordBatchFileReader.new(input)
  fields = reader.schema.fields
  reader.each_with_index do |record_batch, i|
    puts("=" * 40)
    puts("record-batch[#{i}]:")
    fields.each do |field|
      field_name = field.name
      values = record_batch.collect do |record|
        record[field_name]
      end
      puts("  #{field_name}: #{values.inspect}")
    end
  end
end
