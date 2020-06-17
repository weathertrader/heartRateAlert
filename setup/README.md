




# RaceCast 

Create a live leaderboard from gps streaming 

Inline-style: 
![alt text](example.png "hover text")

## Table of Contents
1. [Installation](README.md#installation)
1. [Data Preprocessing](README.md#Data-preprocessing)
1. [Set up database tables](README.md#set-up-database-tables)
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
scp -i ~/.ssh/sundownerwatch-IAM-keypair.pem src/data_preprocess.py ec2-34-222-54-126.us-west-2.compute.amazonaws.com:/home/ubuntu/raceCast/src/.
scp -i ~/.ssh/sundownerwatch-IAM-keypair.pem src/run_preprocess.sh ec2-34-222-54-126.us-west-2.compute.amazonaws.com:/home/ubuntu/raceCast/src/.
scp -i ~/.ssh/sundownerwatch-IAM-keypair.pem data/gps_tracks_subset_by_activity_*.txt ec2-34-222-54-126.us-west-2.compute.amazonaws.com:/home/ubuntu/raceCast/data/.

```
and order the activities by time by running the following 
```
ssh -i ~/.ssh/sundownerwatch-IAM-keypair.pem ec2-34-222-54-126.us-west-2.compute.amazonaws.com
cd raceCast
src/run_preprocess.sh
```
which will write the gps data ordered by timestamp to s3.  If you wish to verify the timestamp ordering 
you can do so with the following on a locally hosted file 
```
head -n 5 gps_stream_total_activities_001_dt_*.csv
tail -n 5 gps_stream_total_activities_001_dt_*.csv
```
## Set up database tables

On the postgres server run the `create_db.py` script to set up the database tables 
```
scp -i ~/.ssh/sundownerwatch-IAM-keypair.pem src/create_db.py ec2-34-222-54-126.us-west-2.compute.amazonaws.com:/home/ubuntu/raceCast/src/.
ssh -i ~/.ssh/sundownerwatch-IAM-keypair.pem ec2-34-222-54-126.us-west-2.compute.amazonaws.com
python src/create_db.py
```
note that you will have to edit and source your .bashrc with the following environmental variables
```
vi .bashrc
export db_name=racecast
export db_host=localhost
export db_user_name=ubuntu
export db_password=''
export db_port=5432
```

and also check that this script works from the Spark master 

```
scp -i ~/.ssh/sundownerwatch-IAM-keypair.pem src/create_db.py ubuntu@ec2-54-202-214-49.us-west-2.compute.amazonaws.com:/home/ubuntu/raceCast/src/.
ssh -i ~/.ssh/sundownerwatch-IAM-keypair.pem ubuntu@ec2-54-202-214-49.us-west-2.compute.amazonaws.com
python src/create_db.py
```
note that in the .bashrc the db_host should now be the ip of the database server 
```
vi .bashrc
export db_name=racecast
export db_host=ec2-34-216-105-134.us-west-2.compute.amazonaws.com
export db_user_name=ubuntu
export db_password= 
export db_port=5432
```












###############################################################################
# Set up Postgres 

# pg server 

ssh ec2-34-222-54-126.us-west-2.compute.amazonaws.com

ubuntu@ec2-34-222-54-126.us-west-2.compute.amazonaws.com

# set up a keypair from local to pg
ssh -i ~/.ssh/sundownerwatch-IAM-keypair.pem ubuntu@ec2-34-222-54-126.us-west-2.compute.amazonaws.com
# set up a keypair from master to pg
ssh -i ~/.ssh/sundownerwatch-IAM-keypair.pem ubuntu@ec2-54-202-214-49.us-west-2.compute.amazonaws.com 'cat ~/.ssh/id_rsa.pub' | ssh -i ~/.ssh/sundownerwatch-IAM-keypair.pem ubuntu@ec2-34-222-54-126.us-west-2.compute.amazonaws.com 'cat >> ~/.ssh/authorized_keys'

# check that you can ssh into pg

# check that you can ssh into pg from master 



scp -i ~/.ssh/sundownerwatch-IAM-keypair.pem src/* ubuntu@ec2-34-222-54-126.us-west-2.compute.amazonaws.com:/home/ubuntu/raceCast/src/.




# now ssh into the server 
ssh -i ~/.ssh/sundownerwatch-IAM-keypair.pem ubuntu@ec2-34-222-54-126.us-west-2.compute.amazonaws.com

# install postgres 
# preferred 
sudo apt-get update && sudo apt upgrade && sudo apt-get install postgresql postgresql-contrib libpq-dev python3-psycopg2
# dont know if this is needed or not 
# sudo apt-get install python3-dev
                                                                                                                                                                        
# deprecated
# sudo apt-get update && sudo apt upgrade && sudo apt install postgresql postgresql-contrib && sudo apt-get install libpq-dev python3-psycopg2 && sudo apt-get install conda

# install miniconda 
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
chmod 755 Miniconda3-latest-Linux-x86_64.sh
source ~/.bashrc
conda update conda 
conda config --add channels conda-forge
conda install -c conda-forge psycopg2 numpy pandas dash 
# pip3 install psycopg2 psycopg2-binary


# edit the .bashrc 

vi ~/.bashrc
export db_name=racecast
export db_host=localhost
export db_user_name=ubuntu
export db_password=' '
export db_port=5432

and 
mkdir ~/.aws
vi ~/.profile 
export AWS_ACCESS_KEY_ID=
export AWS_SECRET_ACCESS_KEY=

and
mkdir .aws
edit .aws/config with appropriate info 
edit .aws/credentials with appropriate info 

and
mkdir -p raceCast/src raceCast/data


# create postgresql user and database
sudo su postgres
psql
CREATE USER ubuntu WITH PASSWORD '';
CREATE DATABASE racecast WITH OWNER ubuntu;
\q

# now send up create_db script and see if it works 
scp -i ~/.ssh/sundownerwatch-IAM-keypair.pem src/create_db.py ubuntu@ec2-34-222-54-126.us-west-2.compute.amazonaws.com:/home/ubuntu/raceCast/src/.
scp -i ~/.ssh/sundownerwatch-IAM-keypair.pem src/*sh ubuntu@ec2-34-222-54-126.us-west-2.compute.amazonaws.com:/home/ubuntu/raceCast/src/.
python src/create_db.py

# now we will check read and insert permissions from the spark master to the pg_server 


# scp the create_db script to the spark master
scp -i ~/.ssh/sundownerwatch-IAM-keypair.pem src/*py ubuntu@ec2-54-202-214-49.us-west-2.compute.amazonaws.com:/home/ubuntu/raceCast/src/.

# ssh into the spark master 
ssh -i ~/.ssh/sundownerwatch-IAM-keypair.pem ubuntu@ec2-54-202-214-49.us-west-2.compute.amazonaws.com

# edit the .bashrc as before but change the db_host from localhost 
export db_host=ec2-34-222-54-126.us-west-2.compute.amazonaws.com


###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################

# check that master can ssh into gp 
ssh ubuntu@ec2-34-222-54-126.us-west-2.compute.amazonaws.com

1 - .conf file on pg and restart 
2 - check security group
3 - check VPC 


# home IP
98.33.42.216




# worker 1
ssh -i ~/.ssh/sundownerwatch-IAM-keypair.pem ubuntu@ec2-54-202-214-49.us-west-2.compute.amazonaws.com 'cat ~/.ssh/id_rsa.pub' | ssh -i ~/.ssh/sundownerwatch-IAM-keypair.pem ubuntu@ec2-18-237-177-6.us-west-2.compute.amazonaws.com 'cat >> ~/.ssh/authorized_keys'
# worker 2
ssh -i ~/.ssh/sundownerwatch-IAM-keypair.pem ubuntu@ec2-54-202-214-49.us-west-2.compute.amazonaws.com 'cat ~/.ssh/id_rsa.pub' | ssh -i ~/.ssh/sundownerwatch-IAM-keypair.pem ubuntu@ec2-34-214-205-202.us-west-2.compute.amazonaws.com 'cat >> ~/.ssh/authorized_keys'
# worker 3 
ssh -i ~/.ssh/sundownerwatch-IAM-keypair.pem ubuntu@ec2-54-202-214-49.us-west-2.compute.amazonaws.com 'cat ~/.ssh/id_rsa.pub' | ssh -i ~/.ssh/sundownerwatch-IAM-keypair.pem ubuntu@ec2-34-215-182-26.us-west-2.compute.amazonaws.com 'cat >> ~/.ssh/authorized_keys'
# ssh keys master -> slave 4 
ssh -i ~/.ssh/sundownerwatch-IAM-keypair.pem ubuntu@ec2-54-202-214-49.us-west-2.compute.amazonaws.com 'cat ~/.ssh/id_rsa.pub' | ssh -i ~/.ssh/sundownerwatch-IAM-keypair.pem ubuntu@ec2-34-219-195-126.us-west-2.compute.amazonaws.com 'cat >> ~/.ssh/authorized_keys'
# ssh keys master -> slave5
ssh -i ~/.ssh/sundownerwatch-IAM-keypair.pem ubuntu@ec2-54-202-214-49.us-west-2.compute.amazonaws.com 'cat ~/.ssh/id_rsa.pub' | ssh -i ~/.ssh/sundownerwatch-IAM-keypair.pem ubuntu@ec2-34-214-104-123.us-west-2.compute.amazonaws.com 'cat >> ~/.ssh/authorized_keys'
# master -> pg
ssh -i ~/.ssh/sundownerwatch-IAM-keypair.pem ubuntu@ec2-54-202-214-49.us-west-2.compute.amazonaws.com 'cat ~/.ssh/id_rsa.pub' | ssh -i ~/.ssh/sundownerwatch-IAM-keypair.pem ubuntu@ec2-34-222-54-126.us-west-2.compute.amazonaws.com 'cat >> ~/.ssh/authorized_keys'





# change data_directory to match above in  
cd /etc/postgresql/10/main
sudo cp postgresql.conf postgresql.conf_old

sudo vi /etc/postgresql/10/main/postgresql.conf
uncomment and set 
listen_addresses=’*’


sudo cp pg_hba.conf pg_hba.conf_old


Add IP to pg_hba.conf
and on the pg_server you'll need to let pg know to listen on all incoming addresses 
# change data_directory to match above in  

sudo vi pg_hba.conf
# Near bottom of file after local rules, add rule (allows remote access):
host    all             all             0.0.0.0/0               md5
host    all		        all		        all			            trust
# what i was doing before under IPV4 connections
# dont do this, not needed
# host    all             all            98.33.42.216/32            md5
# host    all             all  ec2-54-202-214-49.us-west-2.compute.amazonaws.com/32  md5



sudo /etc/init.d/postgresql restart
sudo /etc/init.d/postgresql status
# i think this does not work 
#sudo service postgresql restart
#sudo service postgresql status


# test the connection 

# test remote connection to db 
curl telnet://ec2-34-222-54-126.us-west-2.compute.amazonaws.com:5432

# check connection from local 
psql -U ubuntu -d racecast -p 5432 -h ec2-34-222-54-126.us-west-2.compute.amazonaws.com
# psql -U ubuntu -d racecast -p 5432 -h 34.216.105.134

# test connection from master 
import os
import psycopg2
conn = psycopg2.connect(database=os.environ['db_name'], host='ec2-34-222-54-126.us-west-2.compute.amazonaws.com', user     = os.environ['db_user_name'], password=os.environ['db_password'], port=os.environ['db_port'])    


# add the postgres jar to master and all workers
scp -i ~/.ssh/sundownerwatch-IAM-keypair.pem postgresql-42.2.14.jar ubuntu@ec2-54-202-214-49.us-west-2.compute.amazonaws.com://usr/local/spark/jars/.
scp -i ~/.ssh/sundownerwatch-IAM-keypair.pem postgresql-42.2.14.jar ubuntu@ec2-18-237-177-6.us-west-2.compute.amazonaws.com:/home/ubuntu/.
scp -i ~/.ssh/sundownerwatch-IAM-keypair.pem postgresql-42.2.14.jar ubuntu@ec2-34-214-205-202.us-west-2.compute.amazonaws.com:/home/ubuntu/.
scp -i ~/.ssh/sundownerwatch-IAM-keypair.pem postgresql-42.2.14.jar ubuntu@ec2-34-215-182-26.us-west-2.compute.amazonaws.com:/home/ubuntu/.
scp -i ~/.ssh/sundownerwatch-IAM-keypair.pem postgresql-42.2.14.jar ubuntu@ec2-34-219-195-126.us-west-2.compute.amazonaws.com:/home/ubuntu/.
scp -i ~/.ssh/sundownerwatch-IAM-keypair.pem postgresql-42.2.14.jar ubuntu@ec2-34-214-104-123.us-west-2.compute.amazonaws.com:/home/ubuntu/.

# do i need to edit the .bashrc of all workers with 



and retest from spark instead of python 


# no - dont do chance firewalls 
# on db server as su 
# sudo ufw allow 5432
# sudo ufw allow from ec2-34-222-54-126.us-west-2.compute.amazonaws.com/24 to any port 5432
# sudo ufw allow from ec2-34-222-54-126.us-west-2.compute.amazonaws.com to any port 5432
# sudo ufw allow from 54.202.214.49/24 to any port 5432
# sudo ufw allow from 54.202.214.49 to any port 5432
# sudo ufw allow from 98.33.42.216/24 to any port 5432
# sudo ufw allow from 98.33.42.216 to any port 5432
# sudo ufw show added
# sudo ufw enable
# sudo service postgresql restart


 
# pip3 install spyder‑kernels




general postgresql commands 
space check df –h /var

# launch pg ec2 instance on ec2 
# open all inbound 5432 traffic





check user that postgres runs under
ps aux | grep postgres
user name is postgres
login as user postgres
sudo su - postgres


Remove postgres
sudo apt-get -purge remove postgresql
sudo apt-get -purge remove postgresql-contrib



Stop postgres
sudo service postgresql stop

delete users
sudo userdel importer




conda create -n pg_env
conda activate pg_env




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

# login to psql database
psql -d racecast 


###############################################################################
###############################################################################


## S3 storage setup

bucket name is 
gps-data-processed





## Run Instructions




## To do 



###############################################################################
###############################################################################
# general scp and ssh



rm -rf /usr/local/spark/work/app*


export db_name=racecast
export db_host=ec2-34-222-54-126.us-west-2.compute.amazonaws.com
export db_user_name=ubuntu
export db_password= 
export db_port=5432


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
ssh -i ~/.ssh/sundownerwatch-IAM-keypair.pem ubuntu@ec2-34-222-54-126.us-west-2.compute.amazonaws.com



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
# worker 5
scp -i ~/.ssh/sundownerwatch-IAM-keypair.pem spark-2.4.5-bin-hadoop2.7.tgz ubuntu@ec2-34-214-104-123.us-west-2.compute.amazonaws.com:/home/ubuntu/.








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
conda install -c conda-forge pyspark spyder‑kernels s3fs


# did not install python-dev but may be needed
# sudo apt-get install python3-dev


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

os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.postgresql:postgresql:42.2.14 pyspark-shell'
os.environ['PYSPARK_SUBMIT_ARGS'] = '--driver-class-path /home/craigmatthewsmith/spark-2.4.5-bin-hadoop2.7/jars/postgresql-42.2.14.jar --jars /home/craigmatthewsmith/spark-2.4.5-bin-hadoop2.7/jars/postgresql-42.2.14.jar'
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages /home/craigmatthewsmith/spark-2.4.5-bin-hadoop2.7/jars/postgresql-42.2.14.jar pyspark-shell'



      
# # Returns dataframe column names and data types
# df.dtypes
# # Displays the content of dataframe
# df.show()
# # Return first n rows
# df.head(10)
# # Returns first row
# df.first()
# # Return first n rows
# df.take(5)
# # Computes summary statistics
# df.describe().show()
# # Returns columns of dataframe
# df.columns
# # Counts the number of rows in dataframe
# df.count()
# # Counts the number of distinct rows in dataframe
# df.distinct().count()
# # Prints plans including physical and logical
# df.explain(4)
  
######################################
# write to s3 stuff here 
# df = pd.read_csv('s3://gps-data-processed/gps_stream_3.csv')
# fs = s3fs.S3FileSystem(anon=False)
# fs = s3fs.S3FileSystem(anon=True)
# fs.ls('gps-data-processed')
# fs.touch('gps-data-processed/test.txt') 
# fs.put(file_path,s3_bucket + "/" + rel_path)
# fs = s3fs.S3FileSystem(anon=False, key='<Access Key>', secret='<Secret Key>')

    
    

