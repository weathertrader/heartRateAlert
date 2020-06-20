
# RaceCast Infra Setup

Inline-style: 
![alt text](images/racecast_tech_stack.png "hover text")


## Table of Contents
1. [Postgres Setup](README.md#Postgres-Setup)
1. [Spark Cluster Setup](README.md#spark-cluster-setup)
1. [Connect Spark to Postgres](README.md#Connect-Spark-to-Postgres)
1. [General ssh and scp commands](README.md#General-ssh-and-scp-commands)
1. [Dash setup](README.md#Dash-setup)
1. [Miscellaneous](README.md#Miscellaneous)

## Postgres Setup

Spin up an EC2 instance.  I chose a t2.medium.  Set u a keypair from local to the pg server, and from the Spark master to the pg instance.
Check that you can ssh from master to pg, and from local to pg.  ssh into pg and install postgres, dash and the python ORM to postgres

```
# check that master can ssh into pg 
ssh ubuntu@ec2-34-222-54-126.us-west-2.compute.amazonaws.com
``` 
 
```
sudo apt-get update && sudo apt upgrade && sudo apt-get install postgresql postgresql-contrib libpq-dev python3-psycopg2
```

Install Python from miniconda and packages for communicating the the db and to a Dash server
```
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
chmod 755 Miniconda3-latest-Linux-x86_64.sh
source ~/.bashrc
conda update conda 
conda config --add channels conda-forge
conda install -c conda-forge psycopg2 numpy pandas dash 
```
On the pg_server I install these into the system Python, but on local you may want to put them in a conda environment

```
conda create -n pg_env
conda activate pg_env
```


Follow the directions in the main repo README.md to set up a PG user, database and edit your .bashrc with appropriate environmental variables.
Also be sure to add AWS credentials to your `.profile` and `.aws` files

```
vi ~/.profile 
export AWS_ACCESS_KEY_ID=
export AWS_SECRET_ACCESS_KEY=

and
mkdir .aws

vi .aws/config
[default]
region = us-west-2

vi .aws/credentials
[credentials]
aws_access_key_id=
aws_secret_access_key=

```
Now create the pg user and database

```
sudo su postgres
psql
CREATE USER ubuntu WITH PASSWORD '';
CREATE DATABASE racecast WITH OWNER ubuntu;
\q
```
and execture the `create_db.py` script to make sure it works 
```
python src/create_db.py
```

Now cd to the postgres configuration directory and edit the IP's that postgres will allow and listen on 

```
cd /etc/postgresql/10/main
sudo cp postgresql.conf postgresql.conf_old
sudo vi /etc/postgresql/10/main/postgresql.conf
uncomment and set 
listen_addresses=’*’
```
and
```
sudo cp pg_hba.conf pg_hba.conf_old
sudo vi pg_hba.conf
# Near bottom of file after local rules, add rule (allows remote access):
host    all             all             0.0.0.0/0               md5
host    all		        all		        all			            trust
```
and restart the pg database

```
sudo /etc/init.d/postgresql restart
sudo /etc/init.d/postgresql status
```

Now check that the Spark master can also create tables on the pg database.  Remember to substitute the pg IP in the .bashrc db_host_name.
```
export db_host=ec2-34-222-54-126.us-west-2.compute.amazonaws.com
```
You can also test the connection from local if you postgres setup there
```
psql -U ubuntu -d racecast -p 5432 -h ec2-34-222-54-126.us-west-2.compute.amazonaws.com
```
and that should drop you into a psql prompt.

You can test in the Ipython console from local or Spark master using 

```
import os
import psycopg2
conn = psycopg2.connect(database=os.environ['db_name'], host='ec2-34-222-54-126.us-west-2.compute.amazonaws.com', user     = os.environ['db_user_name'], password=os.environ['db_password'], port=os.environ['db_port'])    
```
If this does not work you'll want to doublecheck your AWS security group Inbound settings

## Spark Cluster Setup

On the master and on all workers, install the following 


sudo apt-get update && sudo apt upgrade
sudo apt-get install openjdk-8-jre-headless
# note here I had to install 11 since 8 did not work 
sudo apt-get install scala
v 2.11.12
scala -version
wget https://downloads.apache.org/spark/spark-2.4.5/spark-2.4.5-bin-hadoop2.7.tgz

tar -xvf spark-2.4.5-bin-hadoop2.7.tgz
sudo mv spark-2.4.5-bin-hadoop2.7/ /usr/local/spark

Now install a python environment which contains pyspake
```
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
chmod 775 that file and execute it then
source ~/.bashrc
conda update conda
conda config --add channels conda-forge
conda install -c conda-forge pyspark
```
On my local machine I use a conda environment for this 
```
conda create -n pyspark_env
conda activate pyspark_env
conda install -c conda-forge pyspark spyder‑kernels s3fs

```

and edit the following files 

```
vi ~/.profile
export PATH=/usr/local/spark/bin:$PATH
export PYSPARK_PYTHON=/home/ubuntu/miniconda3/bin/python3
export PYSPARK_DRIVER_PYTHON=/home/ubuntu/miniconda3/bin/python3
source ~/.profile
```

```
vi ~/.bashrc
export PYSPARK_PYTHON=/home/ubuntu/miniconda3/bin/python3
export PYSPARK_DRIVER_PYTHON=/home/ubuntu/miniconda3/bin/python3

on master 

on local
export PATH=/home/craigmatthewsmith/spark-2.4.5-bin-hadoop2.7/bin:$PATH
export PATH=/usr/local/spark/bin:$PATH
export PYSPARK_PYTHON=/home/craigmatthewsmith/anaconda3/envs/pyspark_env/bin/python3
export PYSPARK_DRIVER_PYTHON=/home/craigmatthewsmith/anaconda3/envs/pyspark_env/bin/python3
export PYSPARK_PYTHON=/home/ubuntu/miniconda3/bin/python3
export PYSPARK_DRIVER_PYTHON=/home/ubuntu/miniconda3/bin/python3
source  ~/.bashrc
```

```
vi /usr/local/spark/conf/spark-env.sh

on master
export SPARK_MASTER_HOST=ec2-54-202-214-49.us-west-2.compute.amazonaws.com
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export PYSPARK_PYTHON=/home/ubuntu/miniconda3/bin/python3
export PYSPARK_DRIVER_PYTHON=/home/ubuntu/miniconda3/bin/python3

on local
vi /usr/local/spark/conf/spark-env.sh
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export PYSPARK_PYTHON=/home/craigmatthewsmith/anaconda3/envs/pyspark_env/bin/python3
export PYSPARK_DRIVER_PYTHON=/home/craigmatthewsmith/anaconda3/envs/pyspark_env/bin/python3

```

and edit `~/.aws/config` and `~/.aws/credentials` as before

Also add the worker IPs to the configuration files 
```
vi /usr/local/spark/conf/slaves
ec2-18-237-177-6.us-west-2.compute.amazonaws.com
ec2-34-214-205-202.us-west-2.compute.amazonaws.com
ec2-34-215-182-26.us-west-2.compute.amazonaws.com
ec2-34-219-195-126.us-west-2.compute.amazonaws.com
ec2-34-214-104-123.us-west-2.compute.amazonaws.com
```

And restart the Spark cluster 
```
on Spark master
bash /usr/local/spark/sbin/start-all.sh
bash /usr/local/spark/sbin/stop-all.sh 
or on local without workers
bash ~/spark-2.4.5-bin-hadoop2.7/sbin/stop-master.sh 
bash ~/spark-2.4.5-bin-hadoop2.7/sbin/stop-slave.sh 
bash ~/spark-2.4.5-bin-hadoop2.7/sbin/start-master.sh 
```
The Spark web UI is availabe on port 8080
http://ec2-54-202-214-49.us-west-2.compute.amazonaws.com:8080


If the Spark cluster runs out of space remove the working application directories
```
rm -rf /usr/local/spark/work/app*
```

## Connect Spark to Postgres

Add the postgres jar to master and all workers
```
scp -i ~/.ssh/sundownerwatch-IAM-keypair.pem postgresql-42.2.14.jar ubuntu@ec2-54-202-214-49.us-west-2.compute.amazonaws.com://usr/local/spark/jars/.
scp -i ~/.ssh/sundownerwatch-IAM-keypair.pem postgresql-42.2.14.jar ubuntu@ec2-18-237-177-6.us-west-2.compute.amazonaws.com:/home/ubuntu/.
scp -i ~/.ssh/sundownerwatch-IAM-keypair.pem postgresql-42.2.14.jar ubuntu@ec2-34-214-205-202.us-west-2.compute.amazonaws.com:/home/ubuntu/.
scp -i ~/.ssh/sundownerwatch-IAM-keypair.pem postgresql-42.2.14.jar ubuntu@ec2-34-215-182-26.us-west-2.compute.amazonaws.com:/home/ubuntu/.
scp -i ~/.ssh/sundownerwatch-IAM-keypair.pem postgresql-42.2.14.jar ubuntu@ec2-34-219-195-126.us-west-2.compute.amazonaws.com:/home/ubuntu/.
scp -i ~/.ssh/sundownerwatch-IAM-keypair.pem postgresql-42.2.14.jar ubuntu@ec2-34-214-104-123.us-west-2.compute.amazonaws.com:/home/ubuntu/.
```

## General ssh and scp commands 

scp -i ~/.ssh/sundownerwatch-IAM-keypair.pem src/create_db.py ec2-34-222-54-126.us-west-2.compute.amazonaws.com:/home/ubuntu/raceCast/src/.
ssh -i ~/.ssh/sundownerwatch-IAM-keypair.pem ec2-34-222-54-126.us-west-2.compute.amazonaws.com
scp -i ~/.ssh/sundownerwatch-IAM-keypair.pem src/create_db.py ubuntu@ec2-54-202-214-49.us-west-2.compute.amazonaws.com:/home/ubuntu/raceCast/src/.
ssh -i ~/.ssh/sundownerwatch-IAM-keypair.pem ubuntu@ec2-54-202-214-49.us-west-2.compute.amazonaws.com

# scp the create_db script to the spark master
scp -i ~/.ssh/sundownerwatch-IAM-keypair.pem src/*py ubuntu@ec2-54-202-214-49.us-west-2.compute.amazonaws.com:/home/ubuntu/raceCast/src/.

# ssh into the spark master 
ssh -i ~/.ssh/sundownerwatch-IAM-keypair.pem ubuntu@ec2-54-202-214-49.us-west-2.compute.amazonaws.com


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


# copy to master 
scp -i ~/.ssh/sundownerwatch-IAM-keypair.pem src/* ubuntu@ec2-54-202-214-49.us-west-2.compute.amazonaws.com:/home/ubuntu/raceCast/src/.
# copy dash app to pg
scp -i ~/.ssh/sundownerwatch-IAM-keypair.pem dash/* ubuntu@ec2-34-222-54-126.us-west-2.compute.amazonaws.com:/home/ubuntu/raceCast/dash/.



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

# pg server 
ssh ec2-34-222-54-126.us-west-2.compute.amazonaws.com
ubuntu@ec2-34-222-54-126.us-west-2.compute.amazonaws.com

# set up a keypair from local to pg
ssh -i ~/.ssh/sundownerwatch-IAM-keypair.pem ubuntu@ec2-34-222-54-126.us-west-2.compute.amazonaws.com
# set up a keypair from master to pg
ssh -i ~/.ssh/sundownerwatch-IAM-keypair.pem ubuntu@ec2-54-202-214-49.us-west-2.compute.amazonaws.com 'cat ~/.ssh/id_rsa.pub' | ssh -i ~/.ssh/sundownerwatch-IAM-keypair.pem ubuntu@ec2-34-222-54-126.us-west-2.compute.amazonaws.com 'cat >> ~/.ssh/authorized_keys'

scp -i ~/.ssh/sundownerwatch-IAM-keypair.pem src/* ubuntu@ec2-34-222-54-126.us-west-2.compute.amazonaws.com:/home/ubuntu/raceCast/src/.

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

scp -i ~/.ssh/sundownerwatch-IAM-keypair.pem src/create_db.py ubuntu@ec2-34-222-54-126.us-west-2.compute.amazonaws.com:/home/ubuntu/raceCast/src/.
scp -i ~/.ssh/sundownerwatch-IAM-keypair.pem src/*sh ubuntu@ec2-34-222-54-126.us-west-2.compute.amazonaws.com:/home/ubuntu/raceCast/src/.

# now ssh into the server 
ssh -i ~/.ssh/sundownerwatch-IAM-keypair.pem ubuntu@ec2-34-222-54-126.us-west-2.compute.amazonaws.com

## Misc

S3 bucket name is `gps-data-processed`

If the Spark workers run out of space delete their working directories 
```
rm -rf /usr/local/spark/work/app*
```
Sid not install python-dev but may be needed
sudo apt-get install python3-dev

sudo apt-get install pip
pip3 install psycopg2
pip3 install psycopg2-binary

# create conda environment for pg
conda create -n pg_env
conda activate pg_env
conda install -c conda-forge psycopg2 numpy pandas
pip install spyder‑kernels

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

dash environment 

conda create -n dash_env
conda activate dash_env
conda install -c conda-forge psycopg2 numpy pandas dash falcon
pip install spyder‑kernels

  
df = pd.read_csv('s3://gps-data-processed/gps_stream_3.csv')
fs = s3fs.S3FileSystem(anon=False)
fs = s3fs.S3FileSystem(anon=True)
fs.ls('gps-data-processed')
fs.touch('gps-data-processed/test.txt') 
fs.put(file_path,s3_bucket + "/" + rel_path)
fs = s3fs.S3FileSystem(anon=False, key='<Access Key>', secret='<Secret Key>')

    
what i was doing before under IPV4 connections
dont do this, not needed
host    all             all            98.33.42.216/32            md5
host    all             all  ec2-54-202-214-49.us-west-2.compute.amazonaws.com/32  md5
    
  
and
mkdir -p raceCast/src raceCast/data

sudo apt-get install python3-dev
  
  
install miniconda 
pip3 install psycopg2 psycopg2-binary


home IP
98.33.42.216








