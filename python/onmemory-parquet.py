from io import BytesIO
import pyarrow as pa
import pyarrow.parquet as pq
import pandas as pd

# オンメモリでarrow_tableをperquet形式にシリアライズする
table = pd.DataFrame( {'a':[x for x in range(10000)]} )
buf = BytesIO()
f = pa.PythonFile(buf)
arrow_table = pa.Table.from_pandas(table)
pq.write_table(arrow_table, f, use_dictionary=False, compression=None)
result = buf.getvalue()
# parquest方式は改行や制御文字を含まないので、このまま、MapReduceなどにかけることができる
print( result )


# オンメモリでbytes型でデータを受け取ったら、pyarrow形式に解釈する

arrow = pq.read_table( pa.BufferReader(result), nthreads=16 )
df = arrow.to_pandas()
print( df.head() )
