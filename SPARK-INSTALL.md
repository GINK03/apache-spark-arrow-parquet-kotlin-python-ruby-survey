# How to download
このサイトから、最新版を適当に落とす  
どうやらJVMだけで動いているようなので、openjdkかoracle-jdkに該当するものが入っている必要がある。　　

最新版は適宜、[サイト](https://spark.apache.org/downloads.html)を確認すること
```cosnole
$ wget https://d3kbcqa49mib13.cloudfront.net/spark-2.2.0-bin-hadoop2.7.tgz
$ tar zxvf spark-2.2.0-bin-hadoop2.7.tgz 
$ sudo ln -s $HOME/spark-2.2.0-bin-hadoop2.7 /usr/local/lib/spark
```

.bashrcにこのような内容を記し、再度読み込む
```console
## add spark home
export SPARK_HOME=/usr/local/lib/spark
export PATH=$SPARK_HOME/bin:$PATH
```

# Install Nightly
欲しい機能のバージョンこそ、入っていなかったりするので、[nightly](https://people.apache.org/~pwendell/spark-nightly/spark-master-bin)をちょくちょく入れる必要がある  
例えば、apache arrowが一部サポートされているのは2.3.0であり、これはnightlyから入れる  

このリンクを消して、再度貼りなおす必要がある
```console
$ sudo rm /usr/local/lib/spark
$ sudo ln -s $HOME/spark-2.3.0-SNAPSHOT /usr/local/lib/spark
```

そして大抵ビルドされていないので、ビルドする  
```console
$ cd spark-2.3.0-SNAPSHOT 
$ mvn package
```

# Python3に切り替える
環境変数で設定できらしい
```console
$ export PYSPARK_PYTHON=python3
```

# Pysparkでファイルを実行する
環境変数に実行ファイルを食わせて実行する
```cosnole
$ PYTHONSTARTUP=${YOUR_CODE} pyspark
```

# Apache Arrowで高速化されたDataFrameの変換の例
```python
from pyspark.sql.functions import rand
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
```
これの実行結果はこのようになる
```console
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
   id         x
0   0  0.164345
1   1  0.477935
2   2  0.940923
```
