#!/bin/bash
#
source ~/.bashrc
source ~/.profile
sleep_interval=5
#echo $sleep_interval

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
