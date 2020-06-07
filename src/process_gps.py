
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


if __name__ == "__main__":
    #if len(sys.argv) != 2:
    #    print("Usage: wordcount <file>", file=sys.stderr)
    #    sys.exit(-1)

    time_start = time.time()
    
    spark = SparkSession\
        .builder\
        .appName("process_gps")\
        .getOrCreate()

    #work_dir      = '/home/craigmatthewsmith/heartRateAlert'
    #file_name_csv = '/home/craigmatthewsmith/heartRateAlert/data/data_temp.csv'
    work_dir = '/home/ubuntu'
    file_name_csv = '/home/ubuntu/data_temp.csv'

    os.chdir(work_dir)
    os.path.isfile(file_name_csv)
    #file_name_text = '/home/craigmatthewsmith/heartRateAlert/data/temp1.txt'

    # create as many worker threads as there are logical cores on master 
    #sc = pyspark.SparkContext('local[*]')

    print('mark01')

    spark = SparkSession\
        .builder\
        .appName("spark_app_name")\
        .getOrCreate()
    
    df = spark.read.format("csv").option("inferSchema",True).option("header", True).load(file_name_csv)
    #df2 = spark.read.load(file_name_csv, format="csv", header="true")
    #display(df)
    #print(df.collect())
    #df.show()
    #df.printSchema()

    print('mark02')
    
    df.createOrReplaceTempView("table_read")

    print('mark03')

    #sql_df = spark.sql("SELECT * FROM table_read ORDER BY user, dt")
    #sql_df = spark.sql("SELECT * FROM table_read ORDER BY dt,user")
    #sql_df.show()

    df_lon_diff = spark.sql("""SELECT user, dt, lon, lon-LAG(lon,1,NULL) OVER (PARTITION BY user ORDER BY dt) \
                               AS lon_diff \
                               FROM table_read""")
    
    df_lat_diff = spark.sql("""SELECT user, dt, lat, lat-LAG(lat,1,NULL) OVER (PARTITION BY user ORDER BY dt) \
                               AS lat_diff \
                               FROM table_read""")

    print('mark04')
    
    #df_lon_diff.show()
    #df_lat_diff.show()

    print('mark10')
    
    df_lat_diff.createOrReplaceTempView("table_lat_diff")
    df_lon_diff.createOrReplaceTempView("table_lon_diff")
    
    # df_lat_diff_abs = spark.sql("""SELECT user, dt, lat, abs(lat_diff) \
    #                            AS abs_lat_diff \
    #                            FROM table_lat_diff""")
    
    # df_lon_diff_abs = spark.sql("""SELECT user, dt, lon, abs(lon_diff) \
    #                            AS abs_lon_diff \
    #                            FROM table_lon_diff""")

    print('mark11')

    df_lat_sum = spark.sql("""SELECT user, sum(abs(lat_diff)) as sum_lat_diff \
                              FROM table_lat_diff GROUP BY (user) \
                               """)

    df_lon_sum = spark.sql("""SELECT user, sum(abs(lon_diff)) as sum_lon_diff \
                              FROM table_lon_diff GROUP BY (user) \
                               """)
    print('mark12')
    
    #df_lat_diff_abs.createOrReplaceTempView("table_lat_diff_abs")
    #df_lon_diff_abs.createOrReplaceTempView("table_lon_diff_abs")
    #df_lat_sum = spark.sql("""SELECT user, sum(abs_lat_diff) as sum_lat_diff \
    #                          FROM table_lat_diff_abs GROUP BY (user) \
    #                           """)
    #df_lon_sum = spark.sql("""SELECT user, sum(abs_lon_diff) as sum_lon_diff \
    #                          FROM table_lon_diff_abs GROUP BY (user) \
    #                           """)
    
    #df_lat_sum.show()
    #df_lon_sum.show()

    print('mark13')
        
    df_lon_first = spark.sql("""SELECT first(user) AS user, first(lon) AS lon_first FROM table_lon_diff GROUP BY user ORDER BY user""")
    df_lon_last  = spark.sql("""SELECT  last(user) AS user,  last(lon) AS lon_last  FROM table_lon_diff GROUP BY user ORDER BY user""")
    df_lat_first = spark.sql("""SELECT first(user) AS user,  last(lat) AS lat_first FROM table_lat_diff GROUP BY user ORDER BY user""")
    df_lat_last  = spark.sql("""SELECT  last(user) AS user,  last(lat) AS lat_last  FROM table_lat_diff GROUP BY user ORDER BY user""")
    df_dt_first  = spark.sql("""SELECT first(user) AS user, first(dt) AS dt_first FROM table_lat_diff GROUP BY user ORDER BY user""")
    df_dt_last   = spark.sql("""SELECT  last(user) AS user,  last(dt) AS dt_last  FROM table_lat_diff GROUP BY user ORDER BY user""")

    print('mark14')

    
    df_processed = df_dt_first.join(df_dt_last,   on=['user'], how='inner') \
                              .join(df_lon_sum,   on=['user'], how='inner') \
                              .join(df_lat_sum,   on=['user'], how='inner') \
                              .join(df_lon_first, on=['user'], how='inner') \
                              .join(df_lon_last,  on=['user'], how='inner') \
                              .join(df_lat_first, on=['user'], how='inner') \
                              .join(df_lat_last,  on=['user'], how='inner')
                               
    print('mark15')
                                
    df_processed.show()


    print('mark16')
    
    
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

#df.drop('_c0').collect()


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
    
    