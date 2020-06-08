
import os
import sys
import numpy as np
from operator import add
from functools import reduce
import csv
import time
import pyspark

from pyspark.sql import SparkSession
from pyspark.sql import SQLContext
from pyspark.sql import Row
from pyspark.sql.functions import abs

#import pyspark.sql.functions as F
from pyspark.sql.window import Window
from pyspark.sql.functions import lag, lead, first, last, desc

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

#host_name = 'local'
host_name = 'master'
#batch_num = 0
#batch_num = 1
batch_num = 2
#batch_num = 3
 
if __name__ == "__main__":
    #if len(sys.argv) != 2:
    #    print("Usage: wordcount <file>", file=sys.stderr)
    #    sys.exit(-1)

    time_start = time.time()
    
    spark = SparkSession\
        .builder\
        .appName("process_gps")\
        .getOrCreate()

    if   (host_name == 'local'):
        base_dir = '/home/craigmatthewsmith'
    elif (host_name == 'master'):
        base_dir = '/home/ubuntu'

    work_dir = os.path.join(base_dir, 'heartRateAlert')
    #file_name_input  = os.path.join(work_dir, 'data', 'gps_stream_'+str(batch_num)+'.csv')
    #file_name_output = os.path.join(work_dir, 'data', 'gps_batch_'+str(batch_num)+'.csv')
    file_name_input  = 's3a://gps-data-processed/gps_stream_'+str(batch_num)+'.csv'
    file_name_output = 's3a://gps-data-processed/gps_batch_' +str(batch_num)+'.csv'
        
    #file_name_csv = '/home/craigmatthewsmith/heartRateAlert/data/data_temp.csv'
        
    #file_name_csv = '/home/craigmatthewsmith/heartRateAlert/data/subset_100.csv'
    #file_name_csv = '/home/craigmatthewsmith/heartRateAlert/data/gps_tracks_processed_0.csv'
    #work_dir = '/home/ubuntu'
    #file_name_csv = '/home/ubuntu/subset_100.csv'
    #file_name_csv = '/home/ubuntu/subset_1000.csv'
    #file_name_csv = '/home/ubuntu/subset_10000.csv'
    #file_name_csv = '/home/ubuntu/subset_100000.csv'
    #file_name_csv = '/home/ubuntu/subset_1000000.csv'
    #file_name_csv = '/home/ubuntu/gps_tracks_processed_0.csv'

    os.chdir(work_dir)
    #os.path.isfile(file_name_csv)
    #file_name_text = '/home/craigmatthewsmith/heartRateAlert/data/temp1.txt'

    # create as many worker threads as there are logical cores on master 
    #sc = pyspark.SparkContext('local[*]')

    print('mark01')

    spark = SparkSession\
        .builder\
        .appName("spark_app_name")\
        .getOrCreate()
    

    print('mark02')

    df = spark.read.format("csv").option("inferSchema",True).option("header", True).load(file_name_input)
    #df2 = spark.read.load(file_name_csv, format="csv", header="true")
    #display(df)
    #print(df.collect())
    #df.show()
    #df.printSchema()
    df = df.drop('_c0')

    print('mark05')
    
    df.createOrReplaceTempView("table_read")

    print('mark06')

    #sql_df = spark.sql("SELECT * FROM table_read ORDER BY user, dt")
    #sql_df = spark.sql("SELECT * FROM table_read ORDER BY dt,user")
    #sql_df.show()

    # df_lon_diff = spark.sql("""SELECT user, dt, lon, lon-LAG(lon,1,NULL) OVER (PARTITION BY user ORDER BY dt) \
    #                            AS lon_diff \
    #                            FROM table_read""")
    
    #df_lat_diff = spark.sql("""SELECT user AS id, dt, lat, lat-LAG(lat,1,NULL) OVER (PARTITION BY user ORDER BY dt) \
    #                            AS lat_diff \
    #                           FROM table_read""")


    df_lon_lat_diff = spark.sql("""SELECT user AS id, dt, \
                               lon, lat, \
                               lon-LAG(lon,1,NULL) OVER (PARTITION BY user ORDER BY dt) \
                               AS lon_diff, \
                               lat-LAG(lat,1,NULL) OVER (PARTITION BY user ORDER BY dt) \
                               AS lat_diff \
                               FROM table_read""")

    print('mark07')
    
    #df_lon_lat_diff.show()
    #df_lat_diff.show()

    print('mark10')
    
    #df_lat_diff.createOrReplaceTempView("table_lat_diff")
    #df_lon_diff.createOrReplaceTempView("table_lon_diff")
    df_lon_lat_diff.createOrReplaceTempView("table_lon_lat_diff")
    
    # df_lat_diff_abs = spark.sql("""SELECT user, dt, lat, abs(lat_diff) \
    #                            AS abs_lat_diff \
    #                            FROM table_lat_diff""")
    
    # df_lon_diff_abs = spark.sql("""SELECT user, dt, lon, abs(lon_diff) \
    #                            AS abs_lon_diff \
    #                            FROM table_lon_diff""")

    print('mark11')

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

    #df_lat_sum = spark.sql("""SELECT user, sum(abs(lat_diff)) as sum_lat_diff \
    #                          FROM table_lat_diff GROUP BY (user) \
    #                           """)

    #df_lon_sum = spark.sql("""SELECT user, sum(abs(lon_diff)) as sum_lon_diff \
    #                          FROM table_lon_diff GROUP BY (user) \
    #                           """)
    print('mark12')
    
    #df_lat_diff_abs.createOrReplaceTempView("table_lat_diff_abs")
    #df_lon_diff_abs.createOrReplaceTempView("table_lon_diff_abs")
    #df_lat_sum = spark.sql("""SELECT user, sum(abs_lat_diff) as sum_lat_diff \
    #                          FROM table_lat_diff_abs GROUP BY (user) \
    #                           """)
    #df_lon_sum = spark.sql("""SELECT user, sum(abs_lon_diff) as sum_lon_diff \
    #                          FROM table_lon_diff_abs GROUP BY (user) \
    #                           """)
    
    #df_lon_sum.show()

    print('mark13')
        
    df_lon_first = spark.sql("""SELECT first(id) AS id, first(lon) AS lon_first FROM table_lon_lat_diff GROUP BY id ORDER BY id""")
    df_lon_last  = spark.sql("""SELECT  last(id) AS id,  last(lon) AS  lon_last FROM table_lon_lat_diff GROUP BY id ORDER BY id""")
    df_lat_first = spark.sql("""SELECT first(id) AS id, first(lat) AS lat_first FROM table_lon_lat_diff GROUP BY id ORDER BY id""")
    df_lat_last  = spark.sql("""SELECT  last(id) AS id,  last(lat) AS  lat_last FROM table_lon_lat_diff GROUP BY id ORDER BY id""")
    df_dt_first  = spark.sql("""SELECT first(id) AS id,  first(dt) AS  dt_first FROM table_lon_lat_diff GROUP BY id ORDER BY id""")
    df_dt_last   = spark.sql("""SELECT  last(id) AS id,   last(dt) AS   dt_last FROM table_lon_lat_diff GROUP BY id ORDER BY id""")

    print('mark14')

    
    df_processed = df_dt_first.join(df_dt_last,     on=['id'], how='inner') \
                              .join(df_lon_lat_sum, on=['id'], how='inner') \
                              .join(df_lon_first,   on=['id'], how='inner') \
                              .join(df_lon_last,    on=['id'], how='inner') \
                              .join(df_lat_first,   on=['id'], how='inner') \
                              .join(df_lat_last,    on=['id'], how='inner')
                               
    print('mark15')
                                
    df_processed.show()

    print('mark16')
    
    df_processed.toPandas().to_csv(file_name_output)    
 
    print('mark17')
    
    time_end = time.time()
    process_dt = (time_end - time_start)/60.0    
    print (f'script took {process_dt:6.3f} minutes ')

#df_first_last = df_lon_first.join(df_lon_last, on=['user'], how='inner') \
#                            .join(df_lat_first, on=['user'], how='inner') \
#                            .join(df_lat_last, on=['user'], how='inner') \
      
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
    
    