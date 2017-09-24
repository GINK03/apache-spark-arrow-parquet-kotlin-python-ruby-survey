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
