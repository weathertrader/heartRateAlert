
# batch_process_gps.py 
# purpose - batch process gps data 
# usage:

import os
import sys
import numpy as np
from operator import add
from functools import reduce
import csv
import time
import pyspark
#import s3fs

#from pyspark import SparkContext
#from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql import SQLContext
from pyspark.sql import Row
from pyspark.sql.functions import abs
from pyspark.sql.window import Window
from pyspark.sql.functions import lag, lead, first, last, desc
import pyspark.sql.functions as F
#from pyspark.sql.functions import *
#from pyspark.sql.functions import explode
#from pyspark.sql.functions import split
#from pyspark.sql.types import *
#from pyspark.streaming import StreamingContext
 
manual_debug = False
#manual_debug = True
if (manual_debug):
    host_name = 'local'
    #host_name = 'master'
    if   (host_name == 'local'):
        base_dir = '/home/craigmatthewsmith'
    elif (host_name == 'pg'):
        base_dir = '/home/ubuntu'
    elif (host_name == 'master'):
        base_dir = '/home/ubuntu'
    work_dir = os.path.join(base_dir, 'raceCast')
    os.chdir(work_dir)
    #file_name_input = 's3a://gps-data-processed/gps_stream_minute_0_1.csv'
    file_name_input = 'data/gps_stream_total_activities_001_dt_00.csv'
else:
    work_dir = os.getcwd()
# work_dir = os.path.join(base_dir, 'raceCast')

#print(os.environ.get('db_name'))
#print(os.environ['db_name'])

# os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.postgresql:postgresql:42.2.14 pyspark-shell'
# os.environ['PYSPARK_SUBMIT_ARGS'] = '--driver-class-path /home/craigmatthewsmith/spark-2.4.5-bin-hadoop2.7/jars/postgresql-42.2.14.jar --jars /home/craigmatthewsmith/spark-2.4.5-bin-hadoop2.7/jars/postgresql-42.2.14.jar'
# os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages /home/craigmatthewsmith/spark-2.4.5-bin-hadoop2.7/jars/postgresql-42.2.14.jar pyspark-shell'

#show_tables = True
show_tables = False

def read_checkpoints(spark, url, properties):
    # this should read only  most recent values in checkpoints or
    # select last value of checkpoints only
    #SELECT timestamp, value, card 
    #FROM my_table 
    #ORDER BY timestamp DESC 
    #LIMIT 1
    
    checkpoints_old_df = spark.read.jdbc(url=url, table='checkpoints', properties=properties)
    #n = 1
    #sql_statement = """SELECT userid, dt, lon_last, lat_last, segment_dist, total_dist FROM checkpoints WHERE userid = 1"""
    #checkpoints_old_df2 = spark.read.format("jdbc").option("url", url).option("user", os.environ['db_user_name']).option("password",os.environ['db_password']).option("driver", "org.postgresql.Driver").option("query", sql_statement).load()
    #checkpoints_old_df2.show()
    return checkpoints_old_df

    # alternative read syntax 
    # driver may not be needed here
    # # .option("dbtable", "checkpoints")
    # checkpoints_old_df3 = spark.read\
    #     .format("jdbc") \
    #     .option("url", url) \
    #     .option("user",     os.environ['db_user_name']) \
    #     .option("password", os.environ['db_password']) \
    #     .option("dbtable",  os.environ['db_name']) \
    #     .option("driver", "org.postgresql.Driver")\
    #     .option("query", query)\
    #     .load()

def read_checkpoints_most_recent(spark, url, properties, db_user_name, db_password):

    #sql_statement = """SELECT DISTINCT ON (userid) userid, dt_last, total_dist \
    #    FROM checkpoints \
    #    ORDER BY userid,total_dist DESC""" 

    #checkpoints_most_recent_df = spark.read\
    #    .format("jdbc") \
    #    .option("url", url) \
    #    .option("user",     os.environ['db_user_name']) \
    #    .option("password", os.environ['db_password']) \
    #    .option("driver", "org.postgresql.Driver")\
    #    .option("query", sql_statement)\
    #    .load()
    #    .option("dbtable",  "checkpoints") \
    sql_statement = """SELECT DISTINCT ON (userid) userid, dt_last, total_dist FROM checkpoints ORDER BY userid,total_dist DESC""" 
    #checkpoints_most_recent_df = spark.read.format("jdbc").option("url", url).option("user", os.environ['db_user_name']).option("password", os.environ['db_password']).option("driver", "org.postgresql.Driver").option("query", sql_statement).load()
    checkpoints_most_recent_df = spark.read.format("jdbc").option("url", url).option("user", db_user_name).option("password", db_password).option("driver", "org.postgresql.Driver").option("query", sql_statement).load()
    #checkpoints_most_recent_df.show()
    return checkpoints_most_recent_df

def update_checkpoints_table(checkpoints_new_to_insert_df, url, properties, start_or_update):
    # may need to append .save()
    mode = 'append'
    checkpoints_new_to_insert_df.write.jdbc(url=url, table='checkpoints', mode=mode, properties=properties)
    # if   (start_or_update == 'start'):
    #     print('update_checkpoints_table start')
    #     #mode = 'overwrite'    
    #     mode = 'append'
    #     checkpoints_new_to_insert_df.write.jdbc(url=url, table='checkpoints', mode=mode, properties=properties)
    # elif (start_or_update == 'update'):
    #     print('update_checkpoints_table update')
    #     # this works
    #     mode = 'append'    
    #     checkpoints_new_to_insert_df.write.jdbc(url=url, table='checkpoints', mode=mode, properties=properties)
    #     # this erases previous entry  
    #     #mode = 'overwrite'    
    #     #checkpoints_new_to_insert_df.write.jdbc(url=url, table='checkpoints', mode=mode, properties=properties)
 
def main(file_name_input, file_name_output, start_or_update):
    
    time_start_all  = time.time()
        
    # configure connections to db from spark     
    url = 'jdbc:postgresql://'+os.environ['db_host']+':'+os.environ['db_port']+'/'+os.environ['db_name']
    print('url is %s' %(url))
    # driver may not be needed
    properties = {'user': os.environ['db_user_name'], 'password': os.environ['db_password'], 'driver': "org.postgresql.Driver"}
    # properties = {
    #     'user':     os.environ['db_user_name'],
    #     'password': os.environ['db_password'],
    #     'driver':   "org.postgresql.Driver",
    # }

    print('start spark session ')
    spark = SparkSession\
        .builder\
        .appName("batch_process_gps")\
        .getOrCreate()
    # .config('spark.driver.extraClassPath','/home/craigmatthewsmith/spark-2.4.5-bin-hadoop2.7/jars/postgresql-42-2.14.jar')\

    #############################################
    # read incoming csv of incoming data  
        
    time_start = time.time()
    print('read csv begin ')
    gps_stream_new_df = spark.read.format("csv").option("inferSchema",True).option("header", True).load(file_name_input)
    print('drop index column')
    gps_stream_new_df = gps_stream_new_df.drop('_c0')
    #print ('showing gps stream csv data')
    #gps_stream_new_df.show()

    # pyspark --packages com.databricks:spark-csv_2.11:1.4.0    
    #schema = StructType([
    #    StructField("sales", IntegerType(),True), 
    #    StructField("sales person", StringType(),True)
    #])
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
    
    # df = spark.read.format("csv").schema(schema).option("header",True).load(file_name_input)
    # df = spark.read.format("com.databricks.spark.csv").schema(schema).option("header",True).load(file_name_input)
    
    #display(df)
    #print(df.collect())
    #df.show()
    #df.printSchema()

    print('read csv end ')

    time_end = time.time()
    process_dt_csv_read = (time_end - time_start)/60.0    


    time_start = time.time()

    print('create checkpoints_new_table')
    gps_stream_new_df.createOrReplaceTempView("gps_stream_new_table")

    # checkpoints_new_df.show()
    #sql_df = spark.sql("SELECT * FROM checkpoints_new_table ORDER BY id, dt")
    #sql_df = spark.sql("SELECT * FROM checkpoints_new_table ORDER BY dt, id")
    #sql_df.show()

    print('compute difference between points ')
    #df_lon_lat_diff = spark.sql("""SELECT id AS id, dt, \
    #                           lon, lat, \
    #                           lon-LAG(lon,1,NULL) OVER (PARTITION BY id ORDER BY dt) \
    #                           AS lon_diff, \
    #                           lat-LAG(lat,1,NULL) OVER (PARTITION BY id ORDER BY dt) \
    #                           AS lat_diff \
    #                           FROM gps_stream_new_table""")

    #df_lon_lat_diff = spark.sql("""SELECT id AS userid, dt, \
    #                           lon, lat, \
    #                           lon-LAG(lon,1,NULL) OVER (PARTITION BY id ORDER BY dt) \
    #                           AS lon_diff, \
    #                           lat-LAG(lat,1,NULL) OVER (PARTITION BY id ORDER BY dt) \
    #                           AS lat_diff \
    #                           FROM gps_stream_new_table
    #                           WHERE id < 1000""")
    

    df_lon_lat_diff = spark.sql("""SELECT id AS userid, dt, \
                                   lon, lat, \
                                   lon-LAG(lon,1,NULL) OVER (PARTITION BY id ORDER BY dt) \
                                   AS lon_diff, \
                                   lat-LAG(lat,1,NULL) OVER (PARTITION BY id ORDER BY dt) \
                                   AS lat_diff \
                                   FROM gps_stream_new_table
                                   WHERE id < 5
                                   ORDER BY id, dt """)

    # df_lon_lat_diff = spark.sql("""SELECT id AS userid, dt, \
    #                                lon, lat, \
    #                                lon-LAG(lon,1,NULL) OVER (PARTITION BY id ORDER BY dt) \
    #                                AS lon_diff, \
    #                                lat-LAG(lat,1,NULL) OVER (PARTITION BY id ORDER BY dt) \
    #                                AS lat_diff \
    #                                FROM gps_stream_new_table
    #                                ORDER BY id, dt """)
        
    #df_lon_lat_diff.show()
    
    print('create table_lon_lat_diff')    
    df_lon_lat_diff.createOrReplaceTempView("table_lon_lat_diff")
    
    #print('compute segment distance ')
    #df_segment_dist = spark.sql("""SELECT userid, \
    #    POWER(POWER(sum(abs(lon_diff)),2)+POWER(sum(abs(lat_diff)),2),0.5)  AS segment_dist \
    #    FROM table_lon_lat_diff GROUP BY (userid)""")
    #df_segment_dist.show()
    #print('create first and last tables')        
    #df_first_and_last = spark.sql("""SELECT FIRST(userid) AS userid, \
    #                                 LAST(dt)  AS   dt_last, \
    #                                 LAST(lon) AS lon_last, \
    #                                 LAST(lat) AS lat_last, \
    #                                 FIRST(lon) AS lon_first, \
    #                                 FIRST(lat) AS lat_first \
    #                                 FROM table_lon_lat_diff GROUP BY userid ORDER BY userid""")
    #print('join tables')   
    #checkpoints_new_df = df_first_and_last.join(df_segment_dist, on=['userid'], how='inner')
    #checkpoints_new_df.show()

    print('compute segment distance and first and last entries in checkpoint ')

    #checkpoints_new_df = spark.sql("""SELECT FIRST(userid) AS userid , \
    #    LAST(dt)   AS   dt_last, \
    #    LAST(lon)  AS  lon_last, \
    #    LAST(lat)  AS  lat_last, \
    #    FIRST(lon) AS lon_first, \
    #    FIRST(lat) AS lat_first, \
    #    POWER(POWER(sum(abs(lon_diff)),2)+POWER(sum(abs(lat_diff)),2),0.5) AS segment_dist \
    #    FROM table_lon_lat_diff GROUP BY userid ORDER BY userid""")
    checkpoints_new_df = spark.sql("""SELECT FIRST(userid) AS userid , \
        LAST(dt)   AS   dt_last, \
        LAST(lon)  AS  lon_last, \
        LAST(lat)  AS  lat_last, \
        FIRST(lon) AS lon_first, \
        FIRST(lat) AS lat_first, \
        100*POWER(POWER(sum(abs(lon_diff)),2)+POWER(sum(abs(lat_diff)),2),0.5) AS segment_dist \
        FROM table_lon_lat_diff GROUP BY userid ORDER BY userid""")

    if (show_tables):
        print ('showing checkpoints_new')
        checkpoints_new_df.show()

    print('create table_checkpoints_new')    
    checkpoints_new_df.createOrReplaceTempView("table_checkpoints_new")
                                
    #checkpoints_new_df.show()
    time_end = time.time()
    process_dt_process_new_checkpoints = (time_end - time_start)/60.0    

    #############################################
    # read checkpoints from db
    time_start = time.time()
    if (start_or_update == 'update'):
        print('read_checkpoints begin')
        (checkpoints_old_df) = read_checkpoints(spark, url, properties)    
        print('read_checkpoints end')
        checkpoints_old_df.createOrReplaceTempView("table_checkpoints_old")                    
        if (show_tables):
            print ('showing checkpoints_old')
            checkpoints_old_df.show()
    time_end = time.time()
    process_dt_read_old_checkpoints = (time_end - time_start)/60.0    


    #############################################
    # read checkpoints most recent from db
    time_start = time.time()
    if (start_or_update == 'update'):
        print('read_checkpoints_most_recent begin')
        (checkpoints_most_recent_df) = read_checkpoints_most_recent(spark, url, properties, os.environ['db_user_name'], os.environ['db_password'])
        print('read_checkpoints_most_recent end')
        checkpoints_most_recent_df.createOrReplaceTempView("table_checkpoints_most_recent")
        if (show_tables):
            print ('showing checkpoints_most_recent')
            checkpoints_most_recent_df.show()
    time_end = time.time()
    process_dt_read_checkpoints_most_recent = (time_end - time_start)/60.0    
            
    #############################################
    # insert checkpoints table with new data 
    time_start = time.time()

    if   (start_or_update == 'start'):
        # checkpoints first time
        checkpoints_new_to_insert_df = spark.sql("""
            SELECT userid, dt_last, lon_last, lat_last, segment_dist, segment_dist AS total_dist \
            FROM table_checkpoints_new""")
    elif (start_or_update == 'update'):
        checkpoints_new_to_insert_df = spark.sql(""" \
            SELECT \
            	table_checkpoints_new.userid, \
            	table_checkpoints_new.dt_last, \
            	table_checkpoints_new.lon_last, \
            	table_checkpoints_new.lat_last, \
            	table_checkpoints_new.segment_dist, \
            	table_checkpoints_new.segment_dist + table_checkpoints_most_recent.total_dist AS total_dist \
            FROM \
            	table_checkpoints_new \
            INNER JOIN table_checkpoints_most_recent ON table_checkpoints_most_recent.userid = table_checkpoints_new.userid \
            ORDER BY table_checkpoints_new.userid""")

    if (show_tables):
        print ('showing checkpoints_new_to_insert_df')
        checkpoints_new_to_insert_df.show()

    print('update_checkpoints_table begin')
    update_checkpoints_table(checkpoints_new_to_insert_df, url, properties, start_or_update)
    print('update_checkpoints_table end')
        
    time_end = time.time()
    process_dt_update_checkpoints = (time_end - time_start)/60.0    
        
    #############################################
    # write to csv 
    time_start = time.time()        

    write_to_csv = False    
    if (write_to_csv):
        print('write to csv begin')
        checkpoints_new_df.toPandas().to_csv(file_name_output)     
        print('write to csv end')    
    time_end = time.time()
    process_dt_write_csv = (time_end - time_start)/60.0    

    time_end_all = time.time()
    process_dt_all = (time_end_all - time_start_all)/60.0    

    # print timing to console 
    print (f'csv_read                took {process_dt_csv_read :6.2f} minutes ')
    print (f'process_new             took {process_dt_process_new_checkpoints  :6.2f} minutes ')
    print (f'read_old_checkpoints    took {process_dt_read_old_checkpoints:6.2f} minutes ')
    print (f'read_checkpoints_recent took {process_dt_read_checkpoints_most_recent:6.2f} minutes ')
    print (f'update_checkpoints      took {process_dt_update_checkpoints:6.2f} minutes ')
    print (f'write                   took {process_dt_write_csv:6.2f} minutes ')
    print (f'all                     took {process_dt_all      :6.2f} minutes ')
    spark.stop()
      
if __name__ == "__main__":
    if (len(sys.argv) != 4):
        print("Usage: python3 batch_process_gps.py file_name_input file_name_output start_or_update", file=sys.stderr)
        sys.exit()
    else:
        file_name_input  = sys.argv[1]  
        file_name_output = sys.argv[2]        
        start_or_update  = sys.argv[3]        
        print('file_name_input  is %s' %(file_name_input))
        print('file_name_output is %s' %(file_name_output))
        print('  start_or_update is %s' %(start_or_update))
        print('calling main before ')
        main(file_name_input, file_name_output, start_or_update)
        print('script executed succesfully ')
        print('script executed succesfully ')



      
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

    
    