
# submit via pyspark-submit on master using s3 hosted data

# batch_process_gps.py 
# purpose - batch process gps data 
# usage:

# spark-submit --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7 --master spark://ec2-54-202-214-49.us-west-2.compute.amazonaws.com:7077 src/batch_process_gps.py s3a://gps-data-processed/gps_stream_0.csv s3a://gps-data-processed/gps_batch_0.csv
# python3 src/batch_process_gps.py s3a://gps-data-processed/gps_stream_0.csv s3a://gps-data-processed/gps_batch_0.csv
# python3 src/batch_process_gps.py data/gps_stream_0.csv data/gps_batch_0.csv
# new files 
# python3 src/batch_process_gps.py data/gps_tracks_stream_minute_0.csv data/gps_tracks_batch_minute_0.csv

# spark-submit local machine local data 
#spark-submit --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7 --master local src/batch_process_gps.py data/gps_tracks_stream_minute_0.csv data/gps_tracks_batch_minute_0.csv


import os
import sys
import numpy as np
from operator import add
from functools import reduce
import csv
import time
import pyspark
#import s3fs

from pyspark.sql import SparkSession
from pyspark.sql import SQLContext
from pyspark.sql import Row
from pyspark.sql.functions import abs
from pyspark.sql.window import Window
from pyspark.sql.functions import lag, lead, first, last, desc

#import pyspark.sql.functions as F
#from pyspark.sql.functions import *
#from pyspark.sql.functions import explode
#from pyspark.sql.functions import split
#from pyspark.sql.types import *
#from pyspark import SparkContext
#from pyspark import SparkConf
#from pyspark.streaming import StreamingContext

# min   local py, ec2 py,  ec2 pspark-submit
# 100     - 0.26    0.37    0.35
# 1000    - 0.36    0.48    0.42  
# 10000   - 0.34    0.58    0.49 
# 100000  - 0.49    0.70    0.55 
# 1000000 - 0.84    1.03    0.71 
# full    - 2.47    2.35    1.08 from local, or 1.33 from S3     

# can process 7M records per 70 sec or 
# 100K records per sec
# 5K records per sec is project min 

# instead of 8 files, want 8*20 = 160 files
# 160 files per min = 2.7 hrs

# have 80M total records
# can process 100K records per sec or 7M records per min for 10 min
# or 4M records per min for 20 min or 66K records per second or 600K participants reporting every 10 sec
# each file should have 4 M records in it arranged by timestamp

host_name = 'local'
#host_name = 'master'
#batch_num = 0
#batch_num = 1
#batch_num = 2
#batch_num = 3
 
manual_debug = False
#manual_debug = True
if (manual_debug):
    if   (host_name == 'local'):
        base_dir = '/home/craigmatthewsmith'
    elif (host_name == 'pg'):
        base_dir = '/home/ubuntu'
    elif (host_name == 'master'):
        base_dir = '/home/ubuntu'
    work_dir = os.path.join(base_dir, 'raceCast')
    os.chdir(work_dir)
else:
    work_dir = os.getcwd()
# work_dir = os.path.join(base_dir, 'raceCast')

#print(os.environ.get('db_name'))
#print(os.environ['db_name'])


def main(file_name_input, file_name_output):
    

    time_start_all = time.time()

    time_start_read = time.time()
    
    print('start spark session ')

    spark = SparkSession\
        .builder\
        .appName("batch_process_gps")\
        .getOrCreate()

    # spark.conf.set("spark.executor.instances", 4)
    # spark.conf.set("spark.executor.cores", 4)

    # create as many worker threads as there are logical cores on master 
    #sc = pyspark.SparkContext('local[*]')

    print('read csv begin ')

    df = spark.read.format("csv").option("inferSchema",True).option("header", True).load(file_name_input)


    # pyspark --packages com.databricks:spark-csv_2.11:1.4.0
    
    # schema = StructType([
    #     StructField("_c0", IntegerType()),
    #     StructField("dt", IntegerType()),
    #     StructField("lon", DoubleType()),
    #     StructField("lat", DoubleType()),
    #     StructField("hr", IntegerType())
    # ])
    
    # # ,dt,id,lon,lat,hr
    # # 0,2000,5509,0.017979517579078674,0.01461024396121502,149
    # # 1,2000,37147,0.02834843471646309,-0.017346767708659172,148
    
    #     df = spark.read.format("csv").schema(schema).option("header",True).load(file_name_input)
    #     df = spark.read.format("com.databricks.spark.csv").schema(schema).option("header",True).load(file_name_input)
    


    #df2 = spark.read.load(file_name_csv, format="csv", header="true")
    #display(df)
    #print(df.collect())
    #df.show()
    #df.printSchema()

    print('read csv end ')

    time_end_read = time.time()
    process_dt_read = (time_end_read - time_start_read)/60.0
    
    time_start_df = time.time()


    print('drop index column')
    df = df.drop('_c0')

    print('create table_read')    
    df.createOrReplaceTempView("table_read")

    #sql_df = spark.sql("SELECT * FROM table_read ORDER BY id, dt")
    #sql_df = spark.sql("SELECT * FROM table_read ORDER BY dt,id")
    #sql_df.show()

    # df_lon_diff = spark.sql("""SELECT id, dt, lon, lon-LAG(lon,1,NULL) OVER (PARTITION BY id ORDER BY dt) \
    #                            AS lon_diff \
    #                            FROM table_read""")
    
    #df_lat_diff = spark.sql("""SELECT id AS id, dt, lat, lat-LAG(lat,1,NULL) OVER (PARTITION BY id ORDER BY dt) \
    #                            AS lat_diff \
    #                           FROM table_read""")

    print('sql select ')
    df_lon_lat_diff = spark.sql("""SELECT id AS id, dt, \
                               lon, lat, \
                               lon-LAG(lon,1,NULL) OVER (PARTITION BY id ORDER BY dt) \
                               AS lon_diff, \
                               lat-LAG(lat,1,NULL) OVER (PARTITION BY id ORDER BY dt) \
                               AS lat_diff \
                               FROM table_read""")

    #df_lon_lat_diff.show()
    #df_lat_diff.show()

    print('create table_lon_lat_diff')
    
    #df_lat_diff.createOrReplaceTempView("table_lat_diff")
    #df_lon_diff.createOrReplaceTempView("table_lon_diff")
    df_lon_lat_diff.createOrReplaceTempView("table_lon_lat_diff")
    
    # df_lat_diff_abs = spark.sql("""SELECT id, dt, lat, abs(lat_diff) \
    #                            AS abs_lat_diff \
    #                            FROM table_lat_diff""")
    
    # df_lon_diff_abs = spark.sql("""SELECT id, dt, lon, abs(lon_diff) \
    #                            AS abs_lon_diff \
    #                            FROM table_lon_diff""")

    print('sql select ')

    df_lon_lat_sum = spark.sql("""SELECT id, \
                              sum(abs(lon_diff)) as sum_lon_diff, \
                              sum(abs(lat_diff)) as sum_lat_diff \
                              FROM table_lon_lat_diff GROUP BY (id) \
                              """)

    #df_lon_lat_sum.show()

    #df_lon_lat_sum = spark.sql("""SELECT id, \ 
    #                              sum(abs(lon_diff)) as sum_lon_diff, \
    #                              sum(abs(lat_diff)) as sum_lat_diff, \
    #                              FROM table_lon_lat_diff GROUP BY (id) \
    #                           """)

    #df_lat_sum = spark.sql("""SELECT id, sum(abs(lat_diff)) as sum_lat_diff \
    #                          FROM table_lat_diff GROUP BY (id) \
    #                           """)

    #df_lon_sum = spark.sql("""SELECT id, sum(abs(lon_diff)) as sum_lon_diff \
    #                          FROM table_lon_diff GROUP BY (id) \
    #                           """)
    
    #df_lat_diff_abs.createOrReplaceTempView("table_lat_diff_abs")
    #df_lon_diff_abs.createOrReplaceTempView("table_lon_diff_abs")
    #df_lat_sum = spark.sql("""SELECT id, sum(abs_lat_diff) as sum_lat_diff \
    #                          FROM table_lat_diff_abs GROUP BY (id) \
    #                           """)
    #df_lon_sum = spark.sql("""SELECT id, sum(abs_lon_diff) as sum_lon_diff \
    #                          FROM table_lon_diff_abs GROUP BY (id) \
    #                           """)
    
    #df_lon_sum.show()

    print('create first and last tables')
        
    df_lon_first = spark.sql("""SELECT first(id) AS id, first(lon) AS lon_first FROM table_lon_lat_diff GROUP BY id ORDER BY id""")
    df_lon_last  = spark.sql("""SELECT  last(id) AS id,  last(lon) AS  lon_last FROM table_lon_lat_diff GROUP BY id ORDER BY id""")
    df_lat_first = spark.sql("""SELECT first(id) AS id, first(lat) AS lat_first FROM table_lon_lat_diff GROUP BY id ORDER BY id""")
    df_lat_last  = spark.sql("""SELECT  last(id) AS id,  last(lat) AS  lat_last FROM table_lon_lat_diff GROUP BY id ORDER BY id""")
    df_dt_first  = spark.sql("""SELECT first(id) AS id,  first(dt) AS  dt_first FROM table_lon_lat_diff GROUP BY id ORDER BY id""")
    df_dt_last   = spark.sql("""SELECT  last(id) AS id,   last(dt) AS   dt_last FROM table_lon_lat_diff GROUP BY id ORDER BY id""")

    print('join tables')

    
    df_processed = df_dt_first.join(df_dt_last,     on=['id'], how='inner') \
                              .join(df_lon_lat_sum, on=['id'], how='inner') \
                              .join(df_lon_first,   on=['id'], how='inner') \
                              .join(df_lon_last,    on=['id'], how='inner') \
                              .join(df_lat_first,   on=['id'], how='inner') \
                              .join(df_lat_last,    on=['id'], how='inner')
                               
    print('process data')
                                
    #df_processed.show()

    time_end_df = time.time()
    process_dt_df = (time_end_df - time_start_df)/60.0    

    print('write to csv begin')
    time_start_write = time.time()

    
    df_processed.toPandas().to_csv(file_name_output)    
 
    print('write to csv end')
    
    time_end_write = time.time()
    process_dt_write = (time_end_write - time_start_write)/60.0    

    time_end_all = time.time()
    process_dt = (time_end_all - time_start_all)/60.0    


    print (f'read    took {process_dt_read :6.2f} minutes ')
    print (f'process took {process_dt_df   :6.2f} minutes ')
    print (f'write   took {process_dt_write:6.2f} minutes ')
    print (f'all     took {process_dt      :6.2f} minutes ')



if __name__ == "__main__":
    if (len(sys.argv) != 3):
        print("Usage: python3 batch_process_gps.py file_name_input file_name_output", file=sys.stderr)
        sys.exit()
    else:
        file_name_input  = sys.argv[1]        
        file_name_output = sys.argv[2]        
        print('file_name_input  is %s' %(file_name_input))
        print('file_name_output is %s' %(file_name_output))
        print('calling main before ')
        main(file_name_input, file_name_output)
        print('script executed succesfully ')




#df_first_last = df_lon_first.join(df_lon_last, on=['id'], how='inner') \
#                            .join(df_lat_first, on=['id'], how='inner') \
#                            .join(df_lat_last, on=['id'], how='inner') \
      
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

# spark = SparkSession.builder \
#     .master("local") \
#     .appName("Word Count") \
#     .config("spark.some.config.option", "some-value") \
#     .getOrCreate()
#     lines = spark.read.text(file_name).rdd.map(lambda r: r[0])
#     counts = lines.flatMap(lambda x: x.split(' ')) \
#                   .map(lambda x: (x, 1)) \
#                   .reduceByKey(add)
#     output = counts.collect()
#     for (word, count) in output:
#         print("%s: %i" % (word, count))

#     spark.stop()
        
######################################
# write to s3 stuff here 
# df = pd.read_csv('s3://gps-data-processed/gps_stream_3.csv')
# fs = s3fs.S3FileSystem(anon=False)
# fs = s3fs.S3FileSystem(anon=True)
# fs.ls('gps-data-processed')
# fs.touch('gps-data-processed/test.txt') 
# fs.put(file_path,s3_bucket + "/" + rel_path)
# fs = s3fs.S3FileSystem(anon=False, key='<Access Key>', secret='<Secret Key>')

    
    