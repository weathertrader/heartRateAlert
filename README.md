

vi /usr/local/spark/conf/slaves

bash /usr/local/spark/sbin/start-all.sh
bash /usr/local/spark/sbin/stop-all.sh 



# connect to postgres in spark 

df.write 
  .format("jdbc") 
  .mode(action)
  .option("url", "jdbc:postgresql://10.0.0.9:5432/"+os.environ['PSQL_DB']) 
  .option("dbtable", table_name) 
  .option("user", os.environ['PSQL_UNAME']) 
  .option("driver", "org.postgresql.Driver")
  .option("password",os.environ['PSQL_PWD'])
  .save()



# on pg 
install python from miniconda and 

sudo apt-get update && sudo apt upgrade
sudo apt install postgresql postgresql-contrib
sudo apt-get install libpq-dev python3-psycopg2
sudo apt-get install conda

# did not install python-dev but may be needed
# sudo apt-get install python3-dev
sudo apt-get install

sudo apt-get install pip
pip3 install psycopg2
# dont know if this is needed or not
pip3 install psycopg2-binary



# create conda environment for pg
conda create -n pg_env
conda activate pg_env
conda install -c conda-forge psycopg2 numpy pandas
pip install spyder‑kernels





# add this to .bashrc
export db_name=racecast
export db_host=localhost
export db_user_name=ubuntu
export db_password=your_password_here
export db_port=5432

# needed for psycopyg2

sudo apt-get install libpq-dev
# did not install python-dev but may be needed
sudo apt-get install python3-dev
sudo apt-get install python3-psycopg2

sudo apt-get install pip
pip3 install psycopg2
# dont know if this is needed or not
pip3 install psycopg2-binary



# create conda environment for pg
conda create -n pg_env
conda activate pg_env
conda install -c conda-forge psycopg2 numpy pandas
pip install spyder‑kernels

conda install -c conda-forge s3fs


sudo apt-get install s3fs




bash ~/spark-2.4.5-bin-hadoop2.7/sbin/start-master.sh 
bash ~/spark-2.4.5-bin-hadoop2.7/sbin/start-slave.sh spark://localhost:7077

bash ~/spark-2.4.5-bin-hadoop2.7/sbin/stop-master.sh 
bash ~/spark-2.4.5-bin-hadoop2.7/sbin/stop-slave.sh 


./spark-2.4.5-bin-hadoop2.7/sbin/start-all.sh
./spark-2.4.5-bin-hadoop2.7/sbin/stop-all.sh


sh /usr/local/spark/sbin/start-all.sh
sh /usr/local/spark/sbin/stop-all.sh 

aws s3 cp s3://gps-data-processed/gps_stream_minute_0_1.csv .

# pg instance 
ec2-34-216-105-134.us-west-2.compute.amazonaws.com
# master - done
ec2-54-202-214-49.us-west-2.compute.amazonaws.com
# slave 1 - done
ec2-18-237-177-6.us-west-2.compute.amazonaws.com
# slave 2 - done
ec2-34-214-205-202.us-west-2.compute.amazonaws.com
# slave 3 - done
ec2-34-215-182-26.us-west-2.compute.amazonaws.com

mkdir -p raceCast/data raceCast/src
# master - done
ssh -i ~/.ssh/sundownerwatch-IAM-keypair.pem ubuntu@ec2-54-202-214-49.us-west-2.compute.amazonaws.com
# slave 1 - done
ssh -i ~/.ssh/sundownerwatch-IAM-keypair.pem ubuntu@ec2-18-237-177-6.us-west-2.compute.amazonaws.com
# slave 2 - done
ssh -i ~/.ssh/sundownerwatch-IAM-keypair.pem ubuntu@ec2-34-214-205-202.us-west-2.compute.amazonaws.com
# slave 3 - done
ssh -i ~/.ssh/sundownerwatch-IAM-keypair.pem ubuntu@ec2-34-215-182-26.us-west-2.compute.amazonaws.com
# pg 
ssh -i ~/.ssh/sundownerwatch-IAM-keypair.pem ubuntu@ec2-34-216-105-134.us-west-2.compute.amazonaws.com


# master - done
scp -i ~/.ssh/sundownerwatch-IAM-keypair.pem data/gps_stream_*.csv ubuntu@ec2-54-202-214-49.us-west-2.compute.amazonaws.com:/home/ubuntu/raceCast/data/.
# slave 1 - done
scp -i ~/.ssh/sundownerwatch-IAM-keypair.pem data/gps_stream_*.csv ubuntu@ec2-18-237-177-6.us-west-2.compute.amazonaws.com:/home/ubuntu/raceCast/data/.
# slave 2 - done
scp -i ~/.ssh/sundownerwatch-IAM-keypair.pem data/gps_stream_*.csv ubuntu@ec2-34-214-205-202.us-west-2.compute.amazonaws.com:/home/ubuntu/raceCast/data/.
# slave 3 - done
scp -i ~/.ssh/sundownerwatch-IAM-keypair.pem data/gps_stream_*.csv ubuntu@ec2-34-215-182-26.us-west-2.compute.amazonaws.com:/home/ubuntu/raceCast/data/.
# pg
scp -i ~/.ssh/sundownerwatch-IAM-keypair.pem data/gps_batch_*.csv ubuntu@ec2-34-216-105-134.us-west-2.compute.amazonaws.com:/home/ubuntu/raceCast/data/.

# master - done
scp -i ~/.ssh/sundownerwatch-IAM-keypair.pem data/gps_tracks_processed_0.csv ubuntu@ec2-54-202-214-49.us-west-2.compute.amazonaws.com:/home/ubuntu/.
# slave 1
scp -i ~/.ssh/sundownerwatch-IAM-keypair.pem data/gps_tracks_processed_0.csv ubuntu@ec2-18-237-177-6.us-west-2.compute.amazonaws.com:/home/ubuntu/.
# slave 2
scp -i ~/.ssh/sundownerwatch-IAM-keypair.pem data/gps_tracks_processed_0.csv ubuntu@ec2-34-214-205-202.us-west-2.compute.amazonaws.com:/home/ubuntu/.
# slave 3 
scp -i ~/.ssh/sundownerwatch-IAM-keypair.pem data/gps_tracks_processed_0.csv ubuntu@ec2-34-215-182-26.us-west-2.compute.amazonaws.com:/home/ubuntu/.


###############################################################################
###############################################################################

# pg instance 
ec2-34-216-105-134.us-west-2.compute.amazonaws.com

ssh -i ~/.ssh/sundownerwatch-IAM-keypair.pem ubuntu@ec2-34-216-105-134.us-west-2.compute.amazonaws.com

# master to pg done 
ssh -i ~/.ssh/sundownerwatch-IAM-keypair.pem ubuntu@ec2-34-216-105-134.us-west-2.compute.amazonaws.com 'cat ~/.ssh/id_rsa.pub' | ssh -i ~/.ssh/sundownerwatch-IAM-keypair.pem ubuntu@ec2-54-202-214-49.us-west-2.compute.amazonaws.com 'cat >> ~/.ssh/authorized_keys'
# pg to master done 
ssh -i ~/.ssh/sundownerwatch-IAM-keypair.pem ubuntu@ec2-54-202-214-49.us-west-2.compute.amazonaws.com 'cat ~/.ssh/id_rsa.pub' | ssh -i ~/.ssh/sundownerwatch-IAM-keypair.pem ubuntu@ec2-34-216-105-134.us-west-2.compute.amazonaws.com 'cat >> ~/.ssh/authorized_keys'

# install pg on pg server 
ssh ubuntu@ec2-54-202-214-49.us-west-2.compute.amazonaws.com
sudo apt-get update && sudo apt upgrade
sudo apt install postgresql postgresql-contrib

sudo su postgres
psql
# to quit
\q 
#createuser --interactive
ubuntu 
# createdb racecast

# login to postgres (as user postgres)
psql 
# quit postgres
\q
# display tables 
\d
\dt 
# list databases
\l 

# List current roles and attributes 
\du
\di 
# Show grant table 
\z



# delete database
DROP DATABASE racecast;

# create postgresql database and tables 
sudo su – postgres
psql
CREATE USER ubuntu WITH PASSWORD '';
CREATE DATABASE racecast WITH OWNER ubuntu;
\q

# login to psql sundowner database
psql -d racecast 




# create tables 
psql example.sql


user
dt_first
dt_last
sum_lon_diff
sum_lat_diff
lon_first
lon_last
lat_first
lat_last


CREATE TABLE leaderboard (
    userid     INT PRIMARY KEY,
    dt         FLOAT  NOT NULL,
    lon_last   FLOAT  NOT NULL, 
    lat_last   FLOAT  NOT NULL, 
    total_dist FLOAT  NOT NULL
);


# change data_directory to match above in  
cd /etc/postgresql/10/main
sudo cp postgresql.conf postgresql.conf_old
sudo vi /etc/postgresql/10/main/postgresql.conf
uncomment listen_addresses=’*’
uncomment or set listen_addresses=’*’

sudo service postgresql restart
sudo service postgresql status

# note done yet 
sudo cp pg_hba.conf pg_hba.conf_old
add IP to the pg_hba.conf

134.197.190.184 – DRI IP address old 
192.168.144.150 – DRI IP address new 
192.168.144.150 

192.168.79.158
Add IP to pg_hba.conf


psql -U postgres -p 5432 -h ec2-34-216-105-134.us-west-2.compute.amazonaws.com














CREATE TABLE leaderboard (
  user       INTEGER PRIMARY KEY,
  dt         FLOAT,
  lon_last   FLOAT, 
  lat_last   FLOAT, 
  total_dist FLOAT);


CREATE TABLE leaderboard (
    user INT PRIMARY KEY,
    dt         FLOAT,
    lon_last   FLOAT, 
    lat_last   FLOAT, 
    total_dist FLOAT, 
    type varchar (50) NOT NULL,
    color varchar (25) NOT NULL,
    location varchar(25) check (location in ('north', 'south', 'west', 'east', 'northeast', 'southeast', 'southwest', 'northwest')),
    install_date date
);



CREATE TABLE batch_diff (
  user       INT4,
  lon_last   FLOAT, 
  lat_last   FLOAT, 
PRIMARY KEY (user);

CREATE TABLE batch_segment (
  user           INT4,
  sum_lon_diff   FLOAT, 
  sum_lat_diff   FLOAT, 
PRIMARY KEY (user);


# drop tables 
DROP TABLE leaderboard;
DROP TABLE batch_diff;
DROP TABLE batch_segment;
# drop all entries in a table 
DELETE from leaderboard;



CREATE TABLE rolling (
  user           INT4,
  dt_first       FLOAT,
  dt_last        FLOAT,
  sum_lon_diff   FLOAT, 
  sum_lat_diff   FLOAT, 
  lon_first      FLOAT, 
  lon_last       FLOAT, 
  lat_first      FLOAT, 
  lat_last       FLOAT, 
PRIMARY KEY (user)
);








## sudo adduser importer
## HkMGWCekuxc3qDWE
## sudo adduser webapp
## t324MymgzUNUpVFY
## sudo su - postgres
psql
CREATE USER importer WITH PASSWORD 'HkMGWCekuxc3qDWE';
CREATE USER webapp WITH PASSWORD 't324MymgzUNUpVFY';
\q
psql -d betterweather
sudo service postgresql restart

GRANT ALL ON ALL TABLES in SCHEMA public TO importer;
GRANT SELECT ON ALL TABLES in SCHEMA public TO webapp;



GRANT SELECT ON stn TO webapp;
GRANT SELECT ON wrf TO webapp;
GRANT SELECT ON obs TO webapp;
Three options here, not sure if 1st works or 2nd works or both or neither, previous effort used last 3 commands 
#GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO importer; 
#GRANT ALL ON stn TO importer;
#GRANT ALL ON wrf TO importer;
#GRANT ALL ON obs TO importer;

general postgresql commands 
space check df –h /var

# launch pg ec2 instance on ec2 
# open all inbound 5432 traffic


#  datetime_valid   TIMESTAMP WITH TIME ZONE,
#  stn_id           VARCHAR(10) REFERENCES stn (id) ON UPDATE CASCADE,
# hgt              FLOAT,
# domain           INT4,
# ensemble_member  VARCHAR(96),
 
 
CREATE TABLE stn (
  id       VARCHAR(10) PRIMARY KEY,
  name     TEXT NOT NULL,
  obs_hgt  FLOAT NOT NULL DEFAULT 10.0,
  mnet_id  INT4,
  lon      DOUBLE PRECISION,
  lat      DOUBLE PRECISION,
  elev     FLOAT,
  notes    TEXT
);



Show contents of table 
SELECT * FROM stn;
sample insert command 
INSERT INTO stn(id, name, obs_hgt, mnet_id, lon, lat, elev, notes) VALUES('KSBA', 'Santa_Barbara_airport', '10.0', '2', '-118.0', '45.0', '100.0', 'note1');
check table contents 
SELECT * FROM stn;
  
Remote connect to db from laptop 
Testing 
psql -U webapp -d makani -h archer.dri.edu
psql -U webapp -d makani -h 138.68.2.68

firewalls 
on db server as su 
sudo ufw allow 5432
sudo ufw allow from 192.168.0.0/24 to any port 5432
sudo ufw show added
sudo ufw enable
sudo ufw allow from 192.168.144.128/24 to any port 5432
sudo ufw allow from 192.168.144.128 to any port 5432

sudo ufw allow from 134.197.190.184/24 to any port 5432
134.197.190.184
sudo ufw allow from 192.168.144.150/24 to any port 5432








DELETE FROM data_hrrr;
DELETE FROM forecasts_downloaded_hrrr
DELETE FROM forecasts_processed_hrrr




Move location of postgres DB from /var/lib to mounted block volume 
# Check current mount point 
sudo -u postgres psql
SHOW data_directory;
\q
# Stop the db 
sudo service postgresql stop
sudo service postgresql status
# move the data over 
sudo rsync -av /var/lib/postgresql /mnt/weathertrader-block-storage
# move the old location to backup
sudo mv /var/lib/postgresql/9.5/main /var/lib/postgresql/9.5/main.bak
sudo chown postgres.postgres /mnt/weathertrader-block-storage/postgresql
# note csmith 03/28/2018 havent done this yet, should free up 10 Gb on the DB server 
sudo rm -rf /var/lib/postgresql/9.5/main.bak




Postgres stuff 
install postgresql 
sudo apt-get install postgresql postgresql-contrib
check user that postgres runs under
ps aux | grep postgres
user name is postgres
login as user postgres
sudo su - postgres


Remove postgres
sudo apt-get -purge remove postgresql
sudo apt-get -purge remove postgresql-contrib



Delete postgres users
DROP USER webapp;

Stop postgres
sudo service postgresql stop

delete users
sudo userdel importer


###############################################################################
###############################################################################



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

## S3 storage setup

bucket name is 
gps-data-processed

## Apache Setup on local

sudo apt-get update && sudo apt upgrade
sudo apt-get install openjdk-8-jre-headless
# note here I had to install 11 since 8 did not work 
sudo apt-get install scala
v 2.11.12
scala -version
wget https://downloads.apache.org/spark/spark-2.4.5/spark-2.4.5-bin-hadoop2.7.tgz

tar -xvf spark-2.4.5-bin-hadoop2.7.tgz
sudo mv spark-2.4.5-bin-hadoop2.7/ /usr/local/spark


/home/craigmatthewsmith/anaconda3/envs/pyspark_env/bin/python3

vi /usr/local/spark/conf/spark-env.sh
export PYSPARK_PYTHON=/home/craigmatthewsmith/anaconda3/envs/pyspark_env/bin/python3
export PYSPARK_DRIVER_PYTHON=/home/craigmatthewsmith/anaconda3/envs/pyspark_env/bin/python3
ec2 only
export SPARK_MASTER_HOST=ec2-54-202-214-49.us-west-2.compute.amazonaws.com
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64


vi ~/.bashrc
export PATH=/home/craigmatthewsmith/spark-2.4.5-bin-hadoop2.7/bin:$PATH
export PYSPARK_PYTHON=/home/craigmatthewsmith/anaconda3/envs/pyspark_env/bin/python3
export PYSPARK_DRIVER_PYTHON=/home/craigmatthewsmith/anaconda3/envs/pyspark_env/bin/python3
ec2 only 
export PATH=/usr/local/spark/bin:$PATH
export PYSPARK_PYTHON=/home/ubuntu/miniconda3/bin/python3
export PYSPARK_DRIVER_PYTHON=/home/ubuntu/miniconda3/bin/python3
and source 


#vi ~/.profile
#export PYSPARK_PYTHON=/home/ubuntu/miniconda3/bin/python3
#export PYSPARK_DRIVER_PYTHON=/home/ubuntu/miniconda3/bin/python3
#and source 



# create conda environment 
conda create -n pyspark_env
conda activate pyspark_env
conda install -c conda-forge pyspark
conda install -c conda-forge spyder‑kernels
conda install -c conda-forge s3fs




## Apache Setup on EC2

ssh into each instance 
```
sudo apt-get update && sudo apt upgrade
sudo apt-get install openjdk-8-jre-headless
sudo apt-get install scala

```
and check the scala version, expecting 2.11.12
```
scala -version
```
on the master install ssh server 
```
# not needed, aleady installed 
sudo apt install openssh-server openssh-client
```
download spark 
```
wget https://downloads.apache.org/spark/spark-2.4.5/spark-2.4.5-bin-hadoop2.7.tgz
```

extract the zipped file to /usr/local/spark and add the spark/bin into PATH variable.

```
tar -xvf spark-2.4.5-bin-hadoop2.7.tgz
sudo mv spark-2.4.5-bin-hadoop2.7/ /usr/local/spark
vi ~/.profile
export PATH=/usr/local/spark/bin:$PATH
source ~/.profile
```

edit the following file 

```
vi /usr/local/spark/conf/spark-env.sh

# contents of conf/spark-env.sh
export SPARK_MASTER_HOST=ec2-54-202-214-49.us-west-2.compute.amazonaws.com
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
# For PySpark use
export PYSPARK_PYTHON=python3
```

and 

```
vi /usr/local/spark/conf/slaves

ec2-18-237-177-6.us-west-2.compute.amazonaws.com
ec2-34-214-205-202.us-west-2.compute.amazonaws.com
ec2-34-215-182-26.us-west-2.compute.amazonaws.com
```

now start and stop the cluster with 

```
sh /usr/local/spark/sbin/start-all.sh
sh /usr/local/spark/sbin/stop-all.sh 

```


install miniconda
```
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
chmod 775 that file and execute it then

source ~/.bashrc

conda update conda
conda config --add channels conda-forge
conda install -c conda-forge pyspark
```

run the examples 

```
python simpleapp.py

spark-submit --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7 --master spark://ec2-54-202-214-49.us-west-2.compute.amazonaws.com simpleapp.py:7077
spark-submit --master spark://ec2-54-202-214-49.us-west-2.compute.amazonaws.com simpleapp.py

spark-submit --master local[4] simpleapp.py

```









vi /usr/local/spark/conf/spark-env.sh
export PYSPARK_PYTHON=/home/ubuntu/miniconda3/bin/python3
export PYSPARK_DRIVER_PYTHON=/home/ubuntu/miniconda3/bin/python3

vi ~/.profile
export PYSPARK_PYTHON=/home/ubuntu/miniconda3/bin/python3
export PYSPARK_DRIVER_PYTHON=/home/ubuntu/miniconda3/bin/python3
and source 

vi ~/.bashrc
export PYSPARK_PYTHON=/home/ubuntu/miniconda3/bin/python3
export PYSPARK_DRIVER_PYTHON=/home/ubuntu/miniconda3/bin/python3
and source 





```


spark-submit --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7 --master spark://ec2-54-202-214-49.us-west-2.compute.amazonaws.com:7077 wordcount.py segment.paths.gz
python wordcount.py segment.paths.gz


spark-submit --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7 --master spark://ec2-54-202-214-49.us-west-2.compute.amazonaws.com:7077 wordcount.py s3a://commoncrawl/crawl-data/CC-MAIN-2020-16/segment.paths.gz


spark-submit --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7 --master spark://ec2-54-202-214-49.us-west-2.compute.amazonaws.com:7077 wordcount.py s3a://commoncrawl/crawl-data/CC-MAIN-2020-16/segment.paths.gz


spark-submit --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7 --master spark://ec2-54-202-214-49.us-west-2.compute.amazonaws.com:7077 wordcount.py s3a://gps-data-processed/segment.paths.gz




does not work
spark-submit --executor-memory 16g --executor-cores 4 --driver-memory 8g --driver-cores 2 --deploy-mode client --master spark://ec2-54-202-214-49.us-west-2.compute.amazonaws.com:7077 wordcount.py segment.paths.gz
spark-submit --executor-memory 4g --executor-cores 2 --driver-memory 4g --driver-cores 2 --deploy-mode client --master spark://ec2-54-202-214-49.us-west-2.compute.amazonaws.com:7077 wordcount.py segment.paths.gz

```


# wordcount w local data
spark-submit --master spark://ec2-54-202-214-49.us-west-2.compute.amazonaws.com:7077 wordcount.py segment.paths.gz
# wordcount w s3data commoncrawl
spark-submit --master spark://ec2-54-202-214-49.us-west-2.compute.amazonaws.com:7077 wordcount.py s3a://commoncrawl/crawl-data/CC-MAIN-2020-16/segment.paths.gz
# wordcount w s3data mine 
spark-submit --master spark://ec2-54-202-214-49.us-west-2.compute.amazonaws.com:7077 wordcount.py s3a://gps-data-processed/segment.paths.gz


spark-submit --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7 --master spark://ec2-54-202-214-49.us-west-2.compute.amazonaws.com:7077 wordcount.py s3a://gps-data-processed/segment.paths.gz



sudo apt-get install python-pip

pip install pyspark


now try running the word count script 
```
spark-submit --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7 --master spark://ec2-54-202-214-49.us-west-2.compute.amazonaws.com:7077 wordcount.py s3a://commoncrawl/crawl-data/CC-MAIN-2020-16/segment.paths.gz
```


http://ec2-54-202-214-49.us-west-2.compute.amazonaws.com:8080





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


scp -i ~/.ssh/sundownerwatch-IAM-keypair.pem src/streaming.py ubuntu@ec2-54-202-214-49.us-west-2.compute.amazonaws.com:/home/ubuntu/.




# master
ssh ubuntu@ec2-54-202-214-49.us-west-2.compute.amazonaws.com

ssh ubuntu@ec2-18-237-177-6.us-west-2.compute.amazonaws.com

ssh ubuntu@ec2-34-214-205-202.us-west-2.compute.amazonaws.com
ssh ubuntu@ec2-34-215-182-26.us-west-2.compute.amazonaws.com



###############################################################################
###############################################################################
Start a multi-core cluster across multiple nodes 
scp the server*.properties to their appropriate nodess

# master
scp -i ~/.ssh/sundownerwatch-IAM-keypair.pem config/server.properties ubuntu@ec2-54-202-214-49.us-west-2.compute.amazonaws.com:/home/ubuntu/kafka_2.12-2.5.0/config/.
# slave 1
scp -i ~/.ssh/sundownerwatch-IAM-keypair.pem config/server-1.properties ubuntu@ec2-18-237-177-6.us-west-2.compute.amazonaws.com:/home/ubuntu/kafka_2.12-2.5.0/config/.
# slave 2
scp -i ~/.ssh/sundownerwatch-IAM-keypair.pem config/server-2.properties ubuntu@ec2-34-214-205-202.us-west-2.compute.amazonaws.com:/home/ubuntu/kafka_2.12-2.5.0/config/.
# slave 3 
scp -i ~/.ssh/sundownerwatch-IAM-keypair.pem config/server-3.properties ubuntu@ec2-34-215-182-26.us-west-2.compute.amazonaws.com:/home/ubuntu/kafka_2.12-2.5.0/config/.

Now start the zookeeper server on master 

```
bin/zookeeper-server-start.sh config/zookeeper.properties
```

Start the kafka servers on master and on slaves 
```
# on master 
bin/kafka-server-start.sh config/server.properties
# on slaves 
bin/kafka-server-start.sh config/server-1.properties
bin/kafka-server-start.sh config/server-2.properties
bin/kafka-server-start.sh config/server-3.properties
```

```
# create topic from master 
bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic test_from_master
# create topic from slave1
bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic test_from_slave1
```

On master and slaves list the topics to make sure they have been generated correctly 
```
# on master
bin/kafka-topics.sh --list --bootstrap-server localhost:9092
# on slaves 
bin/kafka-topics.sh --list --bootstrap-server localhost:9092
```

# works 
#   create topic on master and consume on master
#   create topic on slave  and consume on master
#   create topic on slave  and consume on other slave 

# to check 
#   produce on master and consume on master
#   produce on master and consume on slave
#   produce on slave  and consume on master
#   produce on slave  and produce on master

Now try producing from master or from slave 

```
bin/kafka-console-producer.sh --bootstrap-server localhost:9092 --topic test_from_master
message from master on test_from_master 
bin/kafka-console-producer.sh --bootstrap-server localhost:9092 --topic test_from_slave
message from master on test_from_slave 
```

And consume from master or from slave

```
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --from-beginning --topic test_from_master
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --from-beginning --topic test_from_slave
```

To see which broker is doing what run the describe topics command 

```
bin/kafka-topics.sh --describe --bootstrap-server localhost:9092 --topic test_from_master
bin/kafka-topics.sh --describe --bootstrap-server localhost:9092 --topic test_from_slave1
```

now publish a few messages to our new topic 
```
bin/kafka-console-producer.sh --bootstrap-server localhost:9092 --topic my-replicated-topic
my test message 1
my test message 2
```







###############################################################################
###############################################################################



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


master has switched to one of the followers and node 1 is no longer in the in-sync replica set:

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

```git clone git@github.com:weathertrader/raceCast.git

cd raceCast
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




