# Apache ArrowとApache　PerquetとApache SparkとPandas

## Pandasの限界
Pandasのデータ処理は、コードによるデータのオペレーションを一気に実用に引き上げた印象があります。　　
Pandasの内部はnumpyで記されており、実用的な速度と、SQLより、よりジェネラルに使える様々な機能があります。　　

しかし、Pandasの作者であるWes McKinneyさんによると、[不満点は多い](http://wesmckinney.com/blog/apache-arrow-pandas-internals/)らしく、その指摘箇所は11箇所にも及ぶとのことです。

```
1. Internals too far from "the metal"
2. No support for memory-mapped datasets
3. Poor performance in database and file ingest / export
4. Warty missing data support
5. Lack of transparency into memory use, RAM management
6. Weak support for categorical data
7. Complex groupby operations awkward and slow
8. Appending data to a DataFrame tedious and very costly
9. Limited, non-extensible type metadata
10. Eager evaluation model, no query planning
11. "Slow", limited multicore algorithms for large datasets
```
これらが、Apache Arrowにより解決される様子は、[彼が書いたブログから](http://wesmckinney.com/blog/apache-arrow-pandas-internals/)見れますので確認しておくと良いかと思います。

## Apache Arrowが現在運用されている箇所と、その応用例

Apache Arrowの名前を聞いてからしばらくたちますが、相互運用可能なのは、Python PandasとApache Sparkでの
データ構造の変換が最も役割を果たしているかなという感じで、この[IBMの人の記事](https://arrow.apache.org/blog/2017/07/26/spark-arrow/)によると、
やっとSpark 2.3.0で実装されたようです  

Sparkが標準で採用しているRDDのデータフレームから、Pandasのデータフレームに変換する作業をArrowの機能をOn/Offしていますが、何十倍も差があることがわかるかと思います。　　
```python
17/09/25 07:30:41 WARN Utils: Service 'SparkUI' could not bind on port 4040. Attempting port 4041.
Welcome to
      ____              __
     / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
   /__ / .__/\_,_/_/ /_/\_\   version 2.3.0-SNAPSHOT
      /_/
Using Python version 3.5.2 (default, Aug 18 2017 17:48:00)
SparkSession available as 'spark'.
root
 |-- id: long (nullable = false)
 |-- x: double (nullable = false)
normal elapsed 11.567731857299805 # Apache Arrow使ってない
apache arrow elapsed 0.8107788562774658　 # Apache Arrow使ってる
   id         x
0   0  0.164345
1   1  0.477935
2   2  0.940923
```

このバージョンのSparkはNightlyと呼ばれる安定していないバージョンなので、コンパイル等はされていないので、自分でやる必要があります。　
```console
from pyspark.sql.functions import rand
import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa
import time
df = spark.range(1 << 22).toDF("id").withColumn("x", rand())
df.printSchema()
start = time.time()
pdf = df.toPandas()
print('normal elapsed', time.time() - start)
spark.conf.set("spark.sql.execution.arrow.enable", "true")
start = time.time()
pdf = df.toPandas()
print('apache arrow elapsed', time.time() - start )
print( pdf.head() )
arrow_table = pa.Table.from_pandas(pdf)
pq.write_table(arrow_table, 'local.pq', use_dictionary=False, compression=None)
```

## Python単独でParquetフォーマットを使う
ParquetフォーマットはArrow形式とはまた別のようなものらしいく、圧縮率が高いことを売りにしているのですが、このように、pyarrow(Apache ArrowのPythonでのモジュール名)から呼び出して、読み書きすることができます。  

```python
```

