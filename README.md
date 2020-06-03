
# RaceCast 

Create a live leaderboard from gps streaming 

Inline-style: 
![alt text](example.png "hover text")

## Table of Contents
1. [Kafka Setup](README.md#Kafka-setup
1. [Installation](README.md#installation)
1. [Preprocessing](README.md#preprocessing)
1. [Streaming](README.md#streaming)
1. [Run Instructions](README.md#Run-instructions)
1. [Scripts](README.md#Scripts)
1. [To do](README.md#To-do)
1. [References](README.md#References)



## Kafka Setup

In the EC2 dashboard on AWS, spin up four t2.medium instances, rename three to slave and one to master.
Install passwordless ssh from master to slaves and ssh into the master, update `apt-get` and install `java`. 

```
# master
ssh -i ~/.ssh/sundownerwatch-IAM-keypair.pem ubuntu@ec2-54-202-214-49.us-west-2.compute.amazonaws.com
# slave 1 
ssh -i ~/.ssh/sundownerwatch-IAM-keypair.pem ubuntu@ec2-18-237-177-6.us-west-2.compute.amazonaws.com
# slave 2
ssh -i ~/.ssh/sundownerwatch-IAM-keypair.pem ubuntu@ec2-34-214-205-202.us-west-2.compute.amazonaws.com
# slave 3
ssh -i ~/.ssh/sundownerwatch-IAM-keypair.pem ubuntu@ec2-34-215-182-26.us-west-2.compute.amazonaws.com

sudo apt-get update && sudo apt upgrade
```
check the java version with 
```
java -version
```

and install java8 with 
```
sudo apt-get install openjdk-8-jre-headless
# sudo apt-get install openjdk-8-jdk
# sudo add-apt-repository ppa:linuxuprising/java 
# sudo apt install openjdk-11-jre-headless
```
and recheck the output of `java -version` from the cli.
Now install Kafka  by downloading the zipped file to master, or download to local and scp it to master

```
wget https://downloads.apache.org/kafka/2.5.0/kafka_2.12-2.5.0.tgz
# master
scp -i ~/.ssh/sundownerwatch-IAM-keypair.pem kafka_2.12-2.5.0.tgz ubuntu@ec2-54-202-214-49.us-west-2.compute.amazonaws.com:/home/ubuntu/.
# slave 1
scp -i ~/.ssh/sundownerwatch-IAM-keypair.pem kafka_2.12-2.5.0.tgz ubuntu@ec2-18-237-177-6.us-west-2.compute.amazonaws.com:/home/ubuntu/.
# slave 2
scp -i ~/.ssh/sundownerwatch-IAM-keypair.pem kafka_2.12-2.5.0.tgz ubuntu@ec2-34-214-205-202.us-west-2.compute.amazonaws.com:/home/ubuntu/.
# slave 3 
scp -i ~/.ssh/sundownerwatch-IAM-keypair.pem kafka_2.12-2.5.0.tgz ubuntu@ec2-34-215-182-26.us-west-2.compute.amazonaws.com:/home/ubuntu/.
tar -xzf kafka_2.12-2.5.0.tgz
cd kafka_2.12-2.5.0
```
now start the zookeeper server and then the kafka server (I do this from their own screens)

```
bin/zookeeper-server-start.sh config/zookeeper.properties
bin/kafka-server-start.sh config/server.properties
```

create a topic with 1 partition and 1 replica 
```
bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic test
```
and check that the topic has been created correctly 
```
bin/kafka-topics.sh --list --bootstrap-server localhost:9092
```
send some messages to kafka
```
bin/kafka-console-producer.sh --bootstrap-server localhost:9092 --topic test
This is a message
This is another message
```
start a consumer 
```
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test --from-beginning
This is a message
This is another message
```
To start a multi-core cluster 
```
cp config/server.properties config/server-1.properties 
```
edit the following in the `config/server-1.properties` and repeat for server 2 and 3
by incrementing the id, port and log number 
```    
broker.id=1
listeners=PLAINTEXT://:9093
log.dirs=/tmp/kafka-logs-1
cp config/server-1.properties config/server-2.properties 
cp config/server-1.properties config/server-3.properties 
etc...
```
now start the kafka servers 
```
bin/kafka-server-start.sh config/server-1.properties &
bin/kafka-server-start.sh config/server-2.properties &
bin/kafka-server-start.sh config/server-3.properties
```
Now create a new topic with a replication factor of three:

```
bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 3 --partitions 1 --topic my-replicated-topic
```

To see which broker is doing what run the describe topics command 

```
bin/kafka-topics.sh --describe --bootstrap-server localhost:9092 --topic my-replicated-topic
bin/kafka-topics.sh --describe --bootstrap-server localhost:9092 --topic test
```

now publish a few messages to our new topic 
```
bin/kafka-console-producer.sh --bootstrap-server localhost:9092 --topic my-replicated-topic
my test message 1
my test message 2
```

And consume those messages in another terminal 

```
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --from-beginning --topic my-replicated-topic
```

now lets try killing server 1.  Get the process id and kil it 

```
ps aux | grep server-1.properties
7564 ttys002    0:15.91 ...
kill -9 7564
```


Leadership has switched to one of the followers and node 1 is no longer in the in-sync replica set:

and get the description of the new topic again 
```
bin/kafka-topics.sh --describe --bootstrap-server localhost:9092 --topic my-replicated-topic
```

```
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --from-beginning --topic my-replicated-topic
```

To use Kafka Connect to stream data into our Kafka server, create some test data
```
echo -e "foo\nbar" > test.txt
``` 
and stream the data 
```
bin/connect-standalone.sh config/connect-standalone.properties config/connect-file-source.properties config/connect-file-sink.properties
```
and check the output sink file 
```
more test.sink.txt
```
and check that the data is being stored in the Kafka topic connect-test by running a console consumer to see it 
```
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic connect-test --from-beginning
```

To watch more data move through the pipeline, add another line to our input text file 
```
> echo Another line>> test.txt
```



check the following 

more bin/connect-standalone.sh 
more config/connect-standalone.properties 
more config/connect-file-source.properties 
more config/connect-file-sink.properties


# multi-node set-up 

can add these to the .bashrc 
PATH=$PATH:$HOME/.local/bin:$HOME/bin:$HOME/kafka_2.12-2.0.0/bin 
# on master only 
bin/zookeeper-server-start.sh /home/prashant/kafka_2.12-2.0.0/config/zookeeper.properties> /dev/null 2>&1 & 
kafka_2.12-2.0.0/bin/zookeeper-shell.sh 10.160.0.5:2181 ls /brokers/ids 

# zookeeper.properties 

# the directory where the snapshot is stored.
dataDir=/tmp/zookeeper
# the port at which the clients will connect
clientPort=2181
# disable the per-ip limit on the number of connections since this is a non-production config
maxClientCnxns=0
# Disable the adminserver by default to avoid port conflicts.
# Set the port to something non-conflicting if choosing to enable this
admin.enableServer=false
# admin.serverPort=8080




## Installation

Clone the repo and enter the directory.  

```git clone git@github.com:weathertrader/heartRateAlert.git

cd heartRateAlert
```

Create the python environment and change to it

```conda env create -f environment.yml

conda activate env_gis
```

## Preprocessing 

First download the FitRec dataset `endomondoHR_proper.json` from [this website](https://sites.google.com/eng.ucsd.edu/fitrec-project/home) and move it the `data` directory.
Since the data file is too big to process all at once, we first need to split it up
according the number of cores we wish to stream.  You will need to `cd` into the `data` directory
and `split` the original text file into smaller partitions.

```
cd data
split -l 20000 endomondoHR_proper.json
mv xaa gps_tracks_0.txt 
mv xab gps_tracks_1.txt 
mv xac gps_tracks_2.txt 
mv xad gps_tracks_3.txt 
mv xae gps_tracks_4.txt 
mv xaf gps_tracks_5.txt 
mv xag gps_tracks_6.txt 
mv xah gps_tracks_7.txt 
mv xai gps_tracks_8.txt 
```
Process the data by exectuting the following `bash` script, which in turn will 
call a python script over all of the input files with command line arguments as the input and output data file

```
./src/preprocess.bsh

python src/data_preprocess.py data/gps_tracks_0.txt data/gps_tracks_processed_0.csv
etc ...
```

At this point the data is ordered by timestamp and you can verify with the following command from the cli 
```
head -n 30 gps_tracks_processed_0.csv
```

Now upload these files to S3 using the following command from the cli

```
aws sync command 
```

## Streaming

The data streamer is configured to run on multiple cores simultaneously and the data throughput can be tuned
according to number of cores simultaneously, a delay in starting up each individual core, and a delay on a per-line basis in reading and streaming data
These three command line arguments in order are `n_cores`, `core_delay`, and `line_delay`
From the EC2 cli run one of the following: 

```
python src/produce_stream.py 1 1 0.0

python src/produce_stream.py 8 10 0.001
```

## Run Instructions

Move the example.gpx file into the directory that contains files to process.

`mv example.gpx data/gpx/.`

Process the `gpx` file to geojson


```
python process_all_gpx_to_master.py --dir_gpx=data/gpx --dir_geojson=data/geojson
```

Plot the resulting data in a web browser 

```
python plot_master_geojson.py --dir_geojson=data/geojson
```

## Scripts 

read individual gpx , apply rdp, write to geojson, aggregate all to single with visit counts 
```
process_all_gpx_to_master.py
process_all_gpx_to_master.ipynb
```

plot master geojson tracks and recent individual tracks 
```
plot_master_geojson.py
plot_master_geojson.ipynb

```

## To do 

### Map
1. add junctions 
2. thin points
3. grab tracks via API instead of manually 
4. Fix the master geojson colormap so that saturation occurs at 10 
5. Add RAWS stations

### Track processing
- redo rdp algorithm on individual gpx  
- remove stopped data using speed_min 

## References 
https://github.com/remisalmon/Strava-to-GeoJSON/blob/master/strava_geojson.py
https://github.com/fhirschmann/rdp/blob/master/rdp/__init__.py
https://github.com/sebleier/RDP/blob/master/__init__.py




