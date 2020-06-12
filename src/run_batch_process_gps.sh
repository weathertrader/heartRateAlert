#!/bin/bash
#
source ~/.bashrc
source ~/.profile
sleep_interval=5
#echo $sleep_interval

# default submit script 
spark-submit --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7 --master spark://ec2-54-202-214-49.us-west-2.compute.amazonaws.com:7077 src/batch_process_gps.py s3a://gps-data-processed/gps_stream_minute_0_1.csv s3a://gps-data-processed/gps_batch_dt_00_f_1.csv




# get cores running in script
executor_count = len(spark.sparkContext._jsc.sc().statusTracker().getExecutorInfos()) - 1
cores_per_executor = int(spark.sparkContext.getConf().get('spark.executor.cores','1'))




spark-submit --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7 --master spark://ec2-54-202-214-49.us-west-2.compute.amazonaws.com:7077 src/batch_process_gps.py s3a://gps-data-processed/gps_stream_minute_0_1.csv s3a://gps-data-processed/gps_batch_dt_00_f_1.csv

# default executor cores
spark-submit --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7 --master spark://ec2-54-202-214-49.us-west-2.compute.amazonaws.com:7077 src/batch_process_gps.py s3a://gps-data-processed/gps_stream_minute_0_1.csv s3a://gps-data-processed/gps_batch_dt_00_f_1.csv

# --num-executors 6, 3, 1 does nothing
spark-submit --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7 --master spark://ec2-54-202-214-49.us-west-2.compute.amazonaws.com:7077 --num-executors 6 src/batch_process_gps.py s3a://gps-data-processed/gps_stream_minute_0_1.csv s3a://gps-data-processed/gps_batch_dt_00_f_1.csv

# --executor-cores 1, 3 does not run, 6 does not run
spark-submit --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7 --master spark://ec2-54-202-214-49.us-west-2.compute.amazonaws.com:7077 --executor-cores 1 src/batch_process_gps.py s3a://gps-data-processed/gps_stream_minute_0_1.csv s3a://gps-data-processed/gps_batch_dt_00_f_1.csv

# --num-executors 1
spark-submit --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7 --master spark://ec2-54-202-214-49.us-west-2.compute.amazonaws.com:7077 --num-executors 1 src/batch_process_gps.py s3a://gps-data-processed/gps_stream_minute_0_1.csv s3a://gps-data-processed/gps_batch_dt_00_f_1.csv

# 1, 3, 6 all this 
read    took   0.34 minutes 
process took   0.01 minutes 
write   took   0.70 minutes 
all     took   1.05 minutes 


--total-executor-cores 1
--executor-cores 1 





spark-submit --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7 --master spark://ec2-54-202-214-49.us-west-2.compute.amazonaws.com:7077 src/batch_process_gps.py data/gps_stream_minute_0_1.csv data/gps_batch_dt_00_f_1.csv

aws s3 cp s3://gps-data-processed/gps_stream_minute_0_1.csv  .

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
spark-submit --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7 --master local src/batch_process_gps.py s3a://gps-data-processed/gps_stream_0.csv s3a://gps-data-processed/gps_batch_0.csv
sleep $sleep_interval
spark-submit --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7 --master local src/batch_process_gps.py s3a://gps-data-processed/gps_stream_1.csv s3a://gps-data-processed/gps_batch_1.csv
sleep $sleep_interval
spark-submit --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7 --master local src/batch_process_gps.py s3a://gps-data-processed/gps_stream_2.csv s3a://gps-data-processed/gps_batch_2.csv
sleep $sleep_interval
spark-submit --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7 --master local src/batch_process_gps.py s3a://gps-data-processed/gps_stream_3.csv s3a://gps-data-processed/gps_batch_3.csv
sleep $sleep_interval


spark-submit --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7 --master local src/batch_process_gps.py s3a://gps-data-processed/gps_stream_dt_00_f_1.csv s3a://gps-data-processed/gps_batch_dt_00_f_1.csv


spark-submit --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7 --master local src/batch_process_gps.py s3a://gps-data-processed/gps_stream_minute_0_1.csv s3a://gps-data-processed/gps_batch_dt_00_f_1.csv



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
