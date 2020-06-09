#!/bin/bash
#
sleep_interval=5
echo $sleep_interval

# from s3
python3 src/update_db.py s3://gps-data-processed/gps_batch_0.csv start
sleep $sleep_interval
python3 src/update_db.py s3://gps-data-processed/gps_batch_1.csv update
sleep $sleep_interval
python3 src/update_db.py s3://gps-data-processed/gps_batch_2.csv update
sleep $sleep_interval
python3 src/update_db.py s3://gps-data-processed/gps_batch_3.csv update

# from local
#python3 src/update_db.py data/gps_batch_0.csv start
#sleep $sleep_interval
#python3 src/update_db.py data/gps_batch_1.csv update
#sleep $sleep_interval
#python3 src/update_db.py data/gps_batch_2.csv update
#sleep $sleep_interval
#python3 src/update_db.py data/gps_batch_3.csv update



