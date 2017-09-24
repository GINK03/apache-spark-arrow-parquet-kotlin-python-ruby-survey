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
