#!/bin/bash
#
source ~/.bashrc
source ~/.profile
sleep_interval=2
#echo $sleep_interval

# keiths shuffle partitions command 
# spark.sql.shuffle.partitions=32 

####################################
# master w/ s3 data 
python src/create_db.py
spark-submit --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7 --driver-class-path /usr/local/spark/jars/postgresql-42.2.14.jar --jars /usr/local/spark/jars/postgresql-42.2.14.jar --master spark://ec2-54-202-214-49.us-west-2.compute.amazonaws.com:7077 src/batch_process_gps.py s3a://gps-data-processed/gps_stream_total_activities_010_dt_00.csv s3a://gps-data-processed/gps_batch_total_activities_010_dt_00.csv start
spark-submit --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7 --driver-class-path /usr/local/spark/jars/postgresql-42.2.14.jar --jars /usr/local/spark/jars/postgresql-42.2.14.jar --master spark://ec2-54-202-214-49.us-west-2.compute.amazonaws.com:7077 src/batch_process_gps.py s3a://gps-data-processed/gps_stream_total_activities_010_dt_01.csv s3a://gps-data-processed/gps_batch_total_activities_010_dt_01.csv update
spark-submit --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7 --driver-class-path /usr/local/spark/jars/postgresql-42.2.14.jar --jars /usr/local/spark/jars/postgresql-42.2.14.jar --master spark://ec2-54-202-214-49.us-west-2.compute.amazonaws.com:7077 src/batch_process_gps.py s3a://gps-data-processed/gps_stream_total_activities_010_dt_02.csv s3a://gps-data-processed/gps_batch_total_activities_010_dt_02.csv update
spark-submit --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7 --driver-class-path /usr/local/spark/jars/postgresql-42.2.14.jar --jars /usr/local/spark/jars/postgresql-42.2.14.jar --master spark://ec2-54-202-214-49.us-west-2.compute.amazonaws.com:7077 src/batch_process_gps.py s3a://gps-data-processed/gps_stream_total_activities_010_dt_03.csv s3a://gps-data-processed/gps_batch_total_activities_010_dt_03.csv update
spark-submit --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7 --driver-class-path /usr/local/spark/jars/postgresql-42.2.14.jar --jars /usr/local/spark/jars/postgresql-42.2.14.jar --master spark://ec2-54-202-214-49.us-west-2.compute.amazonaws.com:7077 src/batch_process_gps.py s3a://gps-data-processed/gps_stream_total_activities_010_dt_04.csv s3a://gps-data-processed/gps_batch_total_activities_010_dt_04.csv update
spark-submit --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7 --driver-class-path /usr/local/spark/jars/postgresql-42.2.14.jar --jars /usr/local/spark/jars/postgresql-42.2.14.jar --master spark://ec2-54-202-214-49.us-west-2.compute.amazonaws.com:7077 src/batch_process_gps.py s3a://gps-data-processed/gps_stream_total_activities_010_dt_05.csv s3a://gps-data-processed/gps_batch_total_activities_010_dt_05.csv update
spark-submit --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7 --driver-class-path /usr/local/spark/jars/postgresql-42.2.14.jar --jars /usr/local/spark/jars/postgresql-42.2.14.jar --master spark://ec2-54-202-214-49.us-west-2.compute.amazonaws.com:7077 src/batch_process_gps.py s3a://gps-data-processed/gps_stream_total_activities_010_dt_06.csv s3a://gps-data-processed/gps_batch_total_activities_010_dt_06.csv update
spark-submit --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7 --driver-class-path /usr/local/spark/jars/postgresql-42.2.14.jar --jars /usr/local/spark/jars/postgresql-42.2.14.jar --master spark://ec2-54-202-214-49.us-west-2.compute.amazonaws.com:7077 src/batch_process_gps.py s3a://gps-data-processed/gps_stream_total_activities_010_dt_07.csv s3a://gps-data-processed/gps_batch_total_activities_010_dt_07.csv update
spark-submit --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7 --driver-class-path /usr/local/spark/jars/postgresql-42.2.14.jar --jars /usr/local/spark/jars/postgresql-42.2.14.jar --master spark://ec2-54-202-214-49.us-west-2.compute.amazonaws.com:7077 src/batch_process_gps.py s3a://gps-data-processed/gps_stream_total_activities_010_dt_08.csv s3a://gps-data-processed/gps_batch_total_activities_010_dt_08.csv update
spark-submit --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7 --driver-class-path /usr/local/spark/jars/postgresql-42.2.14.jar --jars /usr/local/spark/jars/postgresql-42.2.14.jar --master spark://ec2-54-202-214-49.us-west-2.compute.amazonaws.com:7077 src/batch_process_gps.py s3a://gps-data-processed/gps_stream_total_activities_010_dt_09.csv s3a://gps-data-processed/gps_batch_total_activities_010_dt_09.csv update
spark-submit --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7 --driver-class-path /usr/local/spark/jars/postgresql-42.2.14.jar --jars /usr/local/spark/jars/postgresql-42.2.14.jar --master spark://ec2-54-202-214-49.us-west-2.compute.amazonaws.com:7077 src/batch_process_gps.py s3a://gps-data-processed/gps_stream_total_activities_010_dt_10.csv s3a://gps-data-processed/gps_batch_total_activities_010_dt_10.csv update



#######################################
# local w/ s3 data  
#/home/craigmatthewsmith/anaconda3/envs/pg_env/bin/python src/create_db.py
#spark-submit --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7 --driver-class-path ~/spark-2.4.5-bin-hadoop2.7/jars/postgresql-42.2.14.jar --jars ~/spark-2.4.5-bin-hadoop2.7/jars/postgresql-42.2.14.jar --master local src/batch_process_gps.py s3a://gps-data-processed/gps_stream_total_activities_001_dt_00.csv s3a://gps-data-processed/gps_batch_total_activities_001_dt_00.csv start
#spark-submit --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7 --driver-class-path ~/spark-2.4.5-bin-hadoop2.7/jars/postgresql-42.2.14.jar --jars ~/spark-2.4.5-bin-hadoop2.7/jars/postgresql-42.2.14.jar --master local src/batch_process_gps.py s3a://gps-data-processed/gps_stream_total_activities_001_dt_01.csv s3a://gps-data-processed/gps_batch_total_activities_001_dt_01.csv update
#spark-submit --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7 --driver-class-path ~/spark-2.4.5-bin-hadoop2.7/jars/postgresql-42.2.14.jar --jars ~/spark-2.4.5-bin-hadoop2.7/jars/postgresql-42.2.14.jar --master local src/batch_process_gps.py s3a://gps-data-processed/gps_stream_total_activities_001_dt_02.csv s3a://gps-data-processed/gps_batch_total_activities_001_dt_02.csv update
#spark-submit --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7 --driver-class-path ~/spark-2.4.5-bin-hadoop2.7/jars/postgresql-42.2.14.jar --jars ~/spark-2.4.5-bin-hadoop2.7/jars/postgresql-42.2.14.jar --master local src/batch_process_gps.py s3a://gps-data-processed/gps_stream_total_activities_001_dt_03.csv s3a://gps-data-processed/gps_batch_total_activities_001_dt_03.csv update
#spark-submit --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7 --driver-class-path ~/spark-2.4.5-bin-hadoop2.7/jars/postgresql-42.2.14.jar --jars ~/spark-2.4.5-bin-hadoop2.7/jars/postgresql-42.2.14.jar --master local src/batch_process_gps.py s3a://gps-data-processed/gps_stream_total_activities_001_dt_04.csv s3a://gps-data-processed/gps_batch_total_activities_001_dt_04.csv update
#spark-submit --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7 --driver-class-path ~/spark-2.4.5-bin-hadoop2.7/jars/postgresql-42.2.14.jar --jars ~/spark-2.4.5-bin-hadoop2.7/jars/postgresql-42.2.14.jar --master local src/batch_process_gps.py s3a://gps-data-processed/gps_stream_total_activities_001_dt_05.csv s3a://gps-data-processed/gps_batch_total_activities_001_dt_05.csv update
#spark-submit --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7 --driver-class-path ~/spark-2.4.5-bin-hadoop2.7/jars/postgresql-42.2.14.jar --jars ~/spark-2.4.5-bin-hadoop2.7/jars/postgresql-42.2.14.jar --master local src/batch_process_gps.py s3a://gps-data-processed/gps_stream_total_activities_001_dt_06.csv s3a://gps-data-processed/gps_batch_total_activities_001_dt_06.csv update
#spark-submit --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7 --driver-class-path ~/spark-2.4.5-bin-hadoop2.7/jars/postgresql-42.2.14.jar --jars ~/spark-2.4.5-bin-hadoop2.7/jars/postgresql-42.2.14.jar --master local src/batch_process_gps.py s3a://gps-data-processed/gps_stream_total_activities_001_dt_07.csv s3a://gps-data-processed/gps_batch_total_activities_001_dt_07.csv update
#spark-submit --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7 --driver-class-path ~/spark-2.4.5-bin-hadoop2.7/jars/postgresql-42.2.14.jar --jars ~/spark-2.4.5-bin-hadoop2.7/jars/postgresql-42.2.14.jar --master local src/batch_process_gps.py s3a://gps-data-processed/gps_stream_total_activities_001_dt_08.csv s3a://gps-data-processed/gps_batch_total_activities_001_dt_08.csv update
#spark-submit --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7 --driver-class-path ~/spark-2.4.5-bin-hadoop2.7/jars/postgresql-42.2.14.jar --jars ~/spark-2.4.5-bin-hadoop2.7/jars/postgresql-42.2.14.jar --master local src/batch_process_gps.py s3a://gps-data-processed/gps_stream_total_activities_001_dt_09.csv s3a://gps-data-processed/gps_batch_total_activities_001_dt_09.csv update
#spark-submit --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7 --driver-class-path ~/spark-2.4.5-bin-hadoop2.7/jars/postgresql-42.2.14.jar --jars ~/spark-2.4.5-bin-hadoop2.7/jars/postgresql-42.2.14.jar --master local src/batch_process_gps.py s3a://gps-data-processed/gps_stream_total_activities_001_dt_10.csv s3a://gps-data-processed/gps_batch_total_activities_001_dt_10.csv update







#######################################
# spark master 
# 0 start master w s3 data
# 1 update master w s3 data
# 2 update master w s3 data
#python src/create_db.py
#spark-submit --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7 --driver-class-path /usr/local/spark/jars/postgresql-42.2.14.jar --jars /usr/local/spark/jars/postgresql-42.2.14.jar --master spark://ec2-54-202-214-49.us-west-2.compute.amazonaws.com:7077 src/batch_process_gps.py s3a://gps-data-processed/gps_stream_total_activities_001_dt_00.csv s3a://gps-data-processed/gps_batch_total_activities_001_dt_00.csv start
#sleep $sleep_interval
#spark-submit --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7 --driver-class-path /usr/local/spark/jars/postgresql-42.2.14.jar --jars /usr/local/spark/jars/postgresql-42.2.14.jar --master spark://ec2-54-202-214-49.us-west-2.compute.amazonaws.com:7077 src/batch_process_gps.py s3a://gps-data-processed/gps_stream_total_activities_008_dt_01.csv s3a://gps-data-processed/gps_batch_total_activities_008_dt_01.csv update
#sleep $sleep_interval
#spark-submit --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7 --driver-class-path /usr/local/spark/jars/postgresql-42.2.14.jar --jars /usr/local/spark/jars/postgresql-42.2.14.jar --master spark://ec2-54-202-214-49.us-west-2.compute.amazonaws.com:7077 src/batch_process_gps.py s3a://gps-data-processed/gps_stream_total_activities_008_dt_02.csv s3a://gps-data-processed/gps_batch_total_activities_008_dt_02.csv update


# ec2 create_db
#sleep $sleep_interval

# 0 start local instance w s3 data
# spark-submit --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7 --driver-class-path ~/spark-2.4.5-bin-hadoop2.7/jars/postgresql-42.2.14.jar --jars ~/spark-2.4.5-bin-hadoop2.7/jars/postgresql-42.2.14.jar --master local src/batch_process_gps.py s3a://gps-data-processed/gps_stream_total_activities_001_dt_00.csv s3a://gps-data-processed/gps_batch_total_activities_001_dt_00.csv start





# 0 start local w local data 
#spark-submit --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7 --driver-class-path ~/spark-2.4.5-bin-hadoop2.7/jars/postgresql-42.2.14.jar --jars ~/spark-2.4.5-bin-hadoop2.7/jars/postgresql-42.2.14.jar --master local src/batch_process_gps.py data/gps_stream_total_activities_001_dt_00.csv data/gps_batch_total_activities_001_dt_00.csv start
#sleep $sleep_interval
# 1 update  local w local data 
#spark-submit --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7 --driver-class-path ~/spark-2.4.5-bin-hadoop2.7/jars/postgresql-42.2.14.jar --jars ~/spark-2.4.5-bin-hadoop2.7/jars/postgresql-42.2.14.jar --master local src/batch_process_gps.py data/gps_stream_total_activities_001_dt_01.csv data/gps_batch_total_activities_001_dt_01.csv update
#sleep $sleep_interval
# 2 update   local w local data
#spark-submit --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7 --driver-class-path ~/spark-2.4.5-bin-hadoop2.7/jars/postgresql-42.2.14.jar --jars ~/spark-2.4.5-bin-hadoop2.7/jars/postgresql-42.2.14.jar --master local src/batch_process_gps.py data/gps_stream_total_activities_001_dt_02.csv data/gps_batch_total_activities_001_dt_02.csv update
#sleep $sleep_interval



# no hardcode full path - try to avoid
#spark-submit --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7 --driver-class-path /home/craigmatthewsmith/spark-2.4.5-bin-hadoop2.7/jars/postgresql-42.2.14.jar --jars /home/craigmatthewsmith/spark-2.4.5-bin-hadoop2.7/jars/postgresql-42.2.14.jar --master local src/batch_process_gps.py data/gps_stream_total_activities_001_dt_00.csv data/gps_batch_total_activities_001_dt_00.csv start
# no 
#--driver-class-path spark-2.4.5-bin-hadoop2.7/jars/postgresql-42.2.14.jar --jars spark-2.4.5-bin-hadoop2.7/jars/postgresql-42.2.14.jar
# no
#--driver-class-path postgresql-42.2.14.jar --jars postgresql-42.2.14.jar

# pyspark --packages org.postgresql:postgresql:42.2.14
# spark-shell --packages org.postgresql:postgresql:42.1.1

# s3 data 
#s3a://gps-data-processed/gps_stream_total_activities_001_dt_00.csv s3a://gps-data-processed/gps_batch_total_activities_001_dt_00.csv

# ec2 spark master 
#--master spark://ec2-54-202-214-49.us-west-2.compute.amazonaws.com:7077 

# default submit script 

# get cores running in script
#executor_count = len(spark.sparkContext._jsc.sc().statusTracker().getExecutorInfos()) - 1
#cores_per_executor = int(spark.sparkContext.getConf().get('spark.executor.cores','1'))

#--num-executors 6
#--executor-cores 1  
#--total-executor-cores 1
#--conf spark.dynamicAllocation.enabled=false --executor-memory 4G --num-executors 10 --executor-cores 2 
#
#aws s3 cp s3://gps-data-processed/gps_stream_minute_0_1.csv  .

# spark-submit ec2 s3
#spark-submit --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7 --master spark://ec2-54-202-214-49.us-west-2.compute.amazonaws.com:7077 src/batch_process_gps.py s3a://gps-data-processed/gps_stream_0.csv s3a://gps-data-processed/gps_batch_0.csv
#sleep $sleep_interval
#spark-submit --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7 --master spark://ec2-54-202-214-49.us-west-2.compute.amazonaws.com:7077 src/batch_process_gps.py s3a://gps-data-processed/gps_stream_1.csv s3a://gps-data-processed/gps_batch_1.csv
#sleep $sleep_interval
#spark-submit --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7 --master spark://ec2-54-202-214-49.us-west-2.compute.amazonaws.com:7077 src/batch_process_gps.py s3a://gps-data-processed/gps_stream_2.csv s3a://gps-data-processed/gps_batch_2.csv
#sleep $sleep_interval
#spark-submit --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7 --master spark://ec2-54-202-214-49.us-west-2.compute.amazonaws.com:7077 src/batch_process_gps.py s3a://gps-data-processed/gps_stream_3.csv s3a://gps-data-processed/gps_batch_3.csv
#leep $sleep_interval

# spark-submit local s3
#spark-submit --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7 --master local src/batch_process_gps.py s3a://gps-data-processed/gps_stream_0.csv s3a://gps-data-processed/gps_batch_0.csv
#sleep $sleep_interval
#spark-submit --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7 --master local src/batch_process_gps.py s3a://gps-data-processed/gps_stream_1.csv s3a://gps-data-processed/gps_batch_1.csv
#sleep $sleep_interval
#spark-submit --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7 --master local src/batch_process_gps.py s3a://gps-data-processed/gps_stream_2.csv s3a://gps-data-processed/gps_batch_2.csv
#sleep $sleep_interval
#spark-submit --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7 --master local src/batch_process_gps.py s3a://gps-data-processed/gps_stream_3.csv s3a://gps-data-processed/gps_batch_3.csv
#sleep $sleep_interval

# from s3
#/home/craigmatthewsmith/anaconda3/envs/pyspark_env/bin/python3 src/batch_process_gps.py s3a://gps-data-processed/gps_stream_0.csv s3a://gps-data-processed/gps_batch_0.csv
#sleep $sleep_interval
#/home/craigmatthewsmith/anaconda3/envs/pyspark_env/bin/python3 src/batch_process_gps.py s3a://gps-data-processed/gps_stream_1.csv s3a://gps-data-processed/gps_batch_1.csv
#sleep $sleep_interval
#/home/craigmatthewsmith/anaconda3/envs/pyspark_env/bin/python3 src/batch_process_gps.py s3a://gps-data-processed/gps_stream_2.csv s3a://gps-data-processed/gps_batch_2.csv
#sleep $sleep_interval
#home/craigmatthewsmith/anaconda3/envs/pyspark_env/bin/python3 src/batch_process_gps.py s3a://gps-data-processed/gps_stream_3.csv s3a://gps-data-processed/gps_batch_3.csv


#python3 src/batch_process_gps.py s3a://gps-data-processed/gps_stream_0.csv s3a://gps-data-processed/gps_batch_0.csv
#sleep $sleep_interval
#python3 src/batch_process_gps.py s3a://gps-data-processed/gps_stream_1.csv s3a://gps-data-processed/gps_batch_1.csv
#sleep $sleep_interval
#python3 src/batch_process_gps.py s3a://gps-data-processed/gps_stream_2.csv s3a://gps-data-processed/gps_batch_2.csv
#sleep $sleep_interval
#python3 src/batch_process_gps.py s3a://gps-data-processed/gps_stream_3.csv s3a://gps-data-processed/gps_batch_3.csv


# from local
#python3 src/batch_process_gps.py data/gps_stream_0.csv data/gps_batch_0.csv
#sleep $sleep_interval
#python3 src/batch_process_gps.py data/gps_stream_1.csv data/gps_batch_1.csv
#leep $sleep_interval
#python3 src/batch_process_gps.py data/gps_stream_2.csv data/gps_batch_2.csv
#sleep $sleep_interval
#python3 src/batch_process_gps.py data/gps_stream_3.csv data/gps_batch_3.csv


# add this to pg instance on ec2
# wget https://jdbc.postgresql.org/download/postgresql-42.2.14.jar
#time spark-submit 

