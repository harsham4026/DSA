cd kafka_2.11-2.0.0
./bin/kafka-server-stop.sh 
vi config/server.properties
./kafka_2.11-2.0.0/bin/kafka-server-start.sh config/server.properties
bin/kafka-server-start.sh config/server.properties
ps aux | grep -i "kafka"
cd kafka_2.11-2.0.0
bin/kafka-topics.sh --list --zookeeper localhost:2181
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic driver --from-beginning
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic user --from-beginning
cd 
tar -zxvf kafka_2.11-2.0.0.tgz 
cd kafka_2.11-2.0.0/
./bin/zookeeper-server-start.sh config/zookeeper.properties
ps aux | grep "zookeeper"
sh bin/kafka-server-start.sh config/server.properties
cd kafka_2.11-2.0.0
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic driver --from-beginning
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic user --from-beginning
 ./kafka_2.11-2.0.0/bin/kafka-server-start.sh config/server.properties
cd kafka_2.11-2.0.0/bin/
ll
./zookeeper-server-stop.sh 
cd
cd /opt/
sudo wget --no-cookies --no-check-certificate --header "Cookie: %3A%2F%2Fwww.oracle.com%2F; -securebackup-cookie" http://download.oracle.com/otn-pub/java/jdk/8u151-b12/e758a0de34e24606bca991d704f6dcbf/jdk-8u151-linux-x64.tar.gz
sudo tar xzf jdk-8u151-linux-x64.tar.gz
ll
sudo tar -zxvf jdk-8u151-linux-x64.tar.gz
sudo tar -zxvf jdk-8u151-linux-x64.tar.gz 
sudo tar xvf jdk-8u151-linux-x64.tar.gz 
 tar xvf jdk-8u151-linux-x64.tar.gz 
ll
sudo su
which gzip
gzip -V
 tar xf jdk-8u151-linux-x64.tar.gz 
cp jdk-8u151-linux-x64.tar.gz jdk-8u151-linux-x64.tar
sudo cp jdk-8u151-linux-x64.tar.gz jdk-8u151-linux-x64.tar
 tar xf jdk-8u151-linux-x64.tar 
 tar -zxvf jdk-8u151-linux-x64.tar 
sudo alternatives --config java
sudo yum update;
sudo yum install java-1.8.0
java -version
sudo alternatives --config java
java -version
cd
cd kafka_2.11-2.0.0
 ./kafka_2.11-2.0.0/bin/zookeeper-server-start.sh config/zookeeper.properties
cd
 ./kafka_2.11-2.0.0/bin/zookeeper-server-start.sh config/zookeeper.properties
 cd kafka_2.11-2.0.0; ./bin/zookeeper-server-start.sh config/zookeeper.properties
ps aux | grep -i kafka
free -m
df 
ps aux | grep -i "zoo"
kill -9 10665
ps aux | grep -i "zoo"
ps aux | grep -i "broker"
ps aux | grep -i "kafka"
cd  kafka_2.11-2.0.0
ll
nohup ./bin/kafka-server-start.sh config/server.properties > mykafkabroker1.out 2>&1
nohup ./bin/kafka-server-start.sh config/server.properties > mykafkabroker1.out 2>&1 &
cd
nohup java -jar kproducer.jar 30 5 90 5 > myproducer.out 2>&1 &
ll
cd kafka_2.11-2.0.0
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic user
ll
cd kafka_2.11-2.0.0
ll
cd ..
cd kafka_2.11-2.0.0
bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic driver
bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic user
bin/kafka-topics.sh --list --zookeeper localhost:2181
cd
ll
java -jar kproducer.jar 30 5 90 5
ll
date
ps aux | grep -i "producer"
python
cd kafka_2.11-2.0.0/
bin/kafka-topics.sh --list --zookeeper localhost:2181
ps aux | grep zookeeper
'
free -m
bin/kafka-topics.sh --list --zookeeper localhost:2181
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic driver
ll
free -m
df
pip install --user confluent-kafka
python
ps aux | grep -i python
ps aux | grep -i "python"

ps aux | grep -i "python"
kill -9 2155
python
pip install kafka-python
pip install --user kafka-python
python
ll
ps aux | grep -i kpro
kill -9 12969
ll
cd kafka_2.11-2.0.0
./bin/kafka-server-stop.sh 
./bin/zookeeper-server-stop.sh 
 nohup ./bin/zookeeper-server-start.sh config/zookeeper.properties myzookeeper.out 2>&1 &
ps aux | grep -i zook
kill -9 12636
ps aux | grep -i zook
 nohup ./bin/zookeeper-server-start.sh config/zookeeper.properties myzookeeper.out 2>&1 &
bin/kafka-console-producer.sh --broker-list localhost:9092 --topic test
bin/kafka-topics.sh --list --zookeeper 13.233.134.2:2181
./bin/zookeeper-server-start.sh config/zookeeper.properties 
ps aux | grep -i zook
 nohup bin/zookeeper-server-start.sh config/zookeeper.properties myzookeeper.out 2>&1 &
ll
ps aux | grep -i zook
 nohup ./bin/zookeeper-server-start.sh config/zookeeper.properties > myzookeeper.out 2>&1 &
ps aux | grep -i zook
bin/kafka-topics.sh --list --zookeeper 13.233.134.2:2181
bin/kafka-topics.sh --list --zookeeper localhost:2181
nohup ./bin/kafka-server-start.sh config/server.properties > mykafkabroker1.out 2>&1 &
tailf mykafkabroker1.out 
cd
nohup java -jar kproducer.jar 30 5 90 5 > myproducer.out 2>&1 &
python
ll
ps aux | grep -i kproducer
kill -9 5810
nohup java -jar kproducer.jar 30 5 90 5 30 > myproducer.out 2>&1 &
tailf myproducer.out 
