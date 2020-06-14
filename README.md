

# RaceCast 

Create a live leaderboard from gps streaming 

Inline-style: 
![alt text](example.png "hover text")

## Table of Contents
1. [Installation](README.md#installation)
1. [Data Preprocessing](README.md#Data-preprocessing)
1. [Streaming](README.md#streaming)
1. [Run Instructions](README.md#Run-instructions)
1. [Scripts](README.md#Scripts)
1. [To do](README.md#To-do)
1. [References](README.md#References)

## Installation

Clone the repo and enter the directory.  

```git clone git@github.com:weathertrader/raceCast.git

cd raceCast
```

Create the python environment and change to it

```conda env create -f environment.yml

conda activate env_gis
```

## Data Preprocessing 

Download the FitRec dataset `endomondoHR_proper.json` from [this website](https://sites.google.com/eng.ucsd.edu/fitrec-project/home) and move it the `data` directory.
Since the data file contains more activities than Spark can handle, we will split the file by activities and order them by time. 

```
src/run_preprocess_split.sh
```
then upload all of the data files and our processing scripts to a remote server on ec2 since we will process them there
```
# aws s3 cp data/ s3://gps-data-processed/ --recursive
scp -i ~/.ssh/sundownerwatch-IAM-keypair.pem src/data_preprocess.py ubuntu@ec2-34-216-105-134.us-west-2.compute.amazonaws.com:/home/ubuntu/raceCast/src/.
scp -i ~/.ssh/sundownerwatch-IAM-keypair.pem src/run_preprocess.sh ubuntu@ec2-34-216-105-134.us-west-2.compute.amazonaws.com:/home/ubuntu/raceCast/src/.
scp -i ~/.ssh/sundownerwatch-IAM-keypair.pem data/gps_tracks_subset_by_activity_*.txt ubuntu@ec2-34-216-105-134.us-west-2.compute.amazonaws.com:/home/ubuntu/raceCast/data/.

```
and order the activities by time by running the following 
```
ssh -i ~/.ssh/sundownerwatch-IAM-keypair.pem ubuntu@ec2-34-216-105-134.us-west-2.compute.amazonaws.com
cd raceCast
src/run_preprocess.sh
```
which will write the gps data ordered by timestamp to s3.  If you wish to verify the timestamp ordering 
you can do so with the following on a locally hosted file 
```
head -n 5 gps_stream_total_activities_001_dt_*.csv
tail -n 5 gps_stream_total_activities_001_dt_*.csv
```



## S3 storage setup

bucket name is 
gps-data-processed




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








###############################################################################
###############################################################################
# general scp and ssh

# worker 4
ec2-34-219-195-126.us-west-2.compute.amazonaws.com
# worker 5
ec2-34-214-104-123.us-west-2.compute.amazonaws.com
# pg instance 
ec2-34-216-105-134.us-west-2.compute.amazonaws.com

# ssh keys master -> slave 4 
ssh -i ~/.ssh/sundownerwatch-IAM-keypair.pem ubuntu@ec2-54-202-214-49.us-west-2.compute.amazonaws.com 'cat ~/.ssh/id_rsa.pub' | ssh -i ~/.ssh/sundownerwatch-IAM-keypair.pem ubuntu@ec2-34-219-195-126.us-west-2.compute.amazonaws.com 'cat >> ~/.ssh/authorized_keys'
# ssh keys master -> slave5
ssh -i ~/.ssh/sundownerwatch-IAM-keypair.pem ubuntu@ec2-54-202-214-49.us-west-2.compute.amazonaws.com 'cat ~/.ssh/id_rsa.pub' | ssh -i ~/.ssh/sundownerwatch-IAM-keypair.pem ubuntu@ec2-34-214-104-123.us-west-2.compute.amazonaws.com 'cat >> ~/.ssh/authorized_keys'

rm -rf /usr/local/spark/work/app*

# master
ssh -i ~/.ssh/sundownerwatch-IAM-keypair.pem ubuntu@ec2-54-202-214-49.us-west-2.compute.amazonaws.com
# worker 1
ssh -i ~/.ssh/sundownerwatch-IAM-keypair.pem ubuntu@ec2-18-237-177-6.us-west-2.compute.amazonaws.com
# worker 2
ssh -i ~/.ssh/sundownerwatch-IAM-keypair.pem ubuntu@ec2-34-214-205-202.us-west-2.compute.amazonaws.com
# worker 3 
ssh -i ~/.ssh/sundownerwatch-IAM-keypair.pem ubuntu@ec2-34-215-182-26.us-west-2.compute.amazonaws.com
# worker 4 
ssh -i ~/.ssh/sundownerwatch-IAM-keypair.pem ubuntu@ec2-34-219-195-126.us-west-2.compute.amazonaws.com
# worker 5 
ssh -i ~/.ssh/sundownerwatch-IAM-keypair.pem ubuntu@ec2-34-214-104-123.us-west-2.compute.amazonaws.com
# pg 
ssh -i ~/.ssh/sundownerwatch-IAM-keypair.pem ubuntu@ec2-34-216-105-134.us-west-2.compute.amazonaws.com

# master  
scp -i ~/.ssh/sundownerwatch-IAM-keypair.pem data/gps_tracks_processed_0.csv ubuntu@ec2-54-202-214-49.us-west-2.compute.amazonaws.com:/home/ubuntu/.
# worker 1
scp -i ~/.ssh/sundownerwatch-IAM-keypair.pem data/gps_tracks_processed_0.csv ubuntu@ec2-18-237-177-6.us-west-2.compute.amazonaws.com:/home/ubuntu/.
# worker 2
scp -i ~/.ssh/sundownerwatch-IAM-keypair.pem data/gps_tracks_processed_0.csv ubuntu@ec2-34-214-205-202.us-west-2.compute.amazonaws.com:/home/ubuntu/.
# worker 3 
scp -i ~/.ssh/sundownerwatch-IAM-keypair.pem data/gps_tracks_processed_0.csv ubuntu@ec2-34-215-182-26.us-west-2.compute.amazonaws.com:/home/ubuntu/.
# worker 4 
scp -i ~/.ssh/sundownerwatch-IAM-keypair.pem spark-2.4.5-bin-hadoop2.7.tgz ubuntu@ec2-34-219-195-126.us-west-2.compute.amazonaws.com:/home/ubuntu/.
# salve 5
scp -i ~/.ssh/sundownerwatch-IAM-keypair.pem spark-2.4.5-bin-hadoop2.7.tgz ubuntu@ec2-34-214-104-123.us-west-2.compute.amazonaws.com:/home/ubuntu/.

# master to pg done 
ssh -i ~/.ssh/sundownerwatch-IAM-keypair.pem ubuntu@ec2-34-216-105-134.us-west-2.compute.amazonaws.com 'cat ~/.ssh/id_rsa.pub' | ssh -i ~/.ssh/sundownerwatch-IAM-keypair.pem ubuntu@ec2-54-202-214-49.us-west-2.compute.amazonaws.com 'cat >> ~/.ssh/authorized_keys'
# pg to master done 
ssh -i ~/.ssh/sundownerwatch-IAM-keypair.pem ubuntu@ec2-54-202-214-49.us-west-2.compute.amazonaws.com 'cat ~/.ssh/id_rsa.pub' | ssh -i ~/.ssh/sundownerwatch-IAM-keypair.pem ubuntu@ec2-34-216-105-134.us-west-2.compute.amazonaws.com 'cat >> ~/.ssh/authorized_keys'



###############################################################################


###############################################################################
##  Spark Setup

sudo apt-get update && sudo apt upgrade
sudo apt-get install openjdk-8-jre-headless
# note here I had to install 11 since 8 did not work 
sudo apt-get install scala
v 2.11.12
scala -version
wget https://downloads.apache.org/spark/spark-2.4.5/spark-2.4.5-bin-hadoop2.7.tgz

tar -xvf spark-2.4.5-bin-hadoop2.7.tgz
sudo mv spark-2.4.5-bin-hadoop2.7/ /usr/local/spark


# install miniconda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
chmod 775 that file and execute it then
source ~/.bashrc
conda update conda
conda config --add channels conda-forge
conda install -c conda-forge pyspark

edit .profile
edit .bashrc
edit .aws/config
edit .aws/credentials

vi /usr/local/spark/conf/spark-env.sh


vi /usr/local/spark/conf/slaves
ec2-18-237-177-6.us-west-2.compute.amazonaws.com
ec2-34-214-205-202.us-west-2.compute.amazonaws.com
ec2-34-215-182-26.us-west-2.compute.amazonaws.com
ec2-34-219-195-126.us-west-2.compute.amazonaws.com
ec2-34-214-104-123.us-west-2.compute.amazonaws.com

vi ~/.profile
export PATH=/usr/local/spark/bin:$PATH
source ~/.profile


edit the following file 


# contents of conf/spark-env.sh
export SPARK_MASTER_HOST=ec2-54-202-214-49.us-west-2.compute.amazonaws.com
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
# For PySpark use
export PYSPARK_PYTHON=python3

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

# set spark paths
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



###############################################################################
# spark start and stop 

http://ec2-54-202-214-49.us-west-2.compute.amazonaws.com:8080

# edit number of workers 
vi /usr/local/spark/conf/slaves

# master spark
bash /usr/local/spark/sbin/start-all.sh
bash /usr/local/spark/sbin/stop-all.sh 
sh /usr/local/spark/sbin/start-all.sh
sh /usr/local/spark/sbin/stop-all.sh 

# local spark
bash ~/spark-2.4.5-bin-hadoop2.7/sbin/start-master.sh 
bash ~/spark-2.4.5-bin-hadoop2.7/sbin/start-slave.sh spark://localhost:7077
bash ~/spark-2.4.5-bin-hadoop2.7/sbin/stop-master.sh 
bash ~/spark-2.4.5-bin-hadoop2.7/sbin/stop-slave.sh 
./spark-2.4.5-bin-hadoop2.7/sbin/start-all.sh
./spark-2.4.5-bin-hadoop2.7/sbin/stop-all.sh

# spark start and stop 
###############################################################################



# create conda environment 
conda create -n pyspark_env
conda activate pyspark_env
conda install -c conda-forge pyspark
conda install -c conda-forge spyder‑kernels
conda install -c conda-forge s3fs

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



###############################################################################
# dash 
conda create -n dash_env
conda activate dash_env
conda install -c conda-forge psycopg2 numpy pandas dash falcon
pip install spyder‑kernels

# dash
###############################################################################


###############################################################################
# pg

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


psql
CREATE USER importer WITH PASSWORD '';
CREATE USER webapp WITH PASSWORD '';
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



