# batch_process_gps.py 
# purpose: batch process gps data into checkpoints and insert to db
# usage: spark-submit --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7 --driver-class-path /usr/local/spark/jars/postgresql-42.2.14.jar --jars /usr/local/spark/jars/postgresql-42.2.14.jar --master spark://ec2-54-202-214-49.us-west-2.compute.amazonaws.com:7077 src/batch_process_gps.py s3a://gps-data-processed/gps_stream_total_activities_001_dt_00.csv s3a://gps-data-processed/gps_batch_total_activities_001_dt_00.csv start

import os
import sys
import numpy as np
import time
#import s3fs

#import pyspark
#from pyspark import SparkContext
#from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.types import *
#from pyspark.sql.types import StructType

#from pyspark.sql import SQLContext
#from pyspark.sql import Row
#from pyspark.sql.functions import abs
#from pyspark.sql.window import Window
#from pyspark.sql.functions import lag, lead, first, last, desc
#import pyspark.sql.functions as F
#from pyspark.sql.functions import *
#from pyspark.sql.functions import explode
#from pyspark.sql.functions import split
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

# print tables to consolse
#show_tables = True
show_tables = False

def read_checkpoints(spark, url, properties):    
    checkpoints_old_df = spark.read.jdbc(url=url, table='checkpoints', properties=properties)
    return checkpoints_old_df

def read_checkpoints_most_recent(spark, url, properties, db_user_name, db_password):
    #sql_statement = """SELECT DISTINCT ON (userid) userid, dt_last, total_dist \
    #    FROM checkpoints \
    #    ORDER BY userid,total_dist DESC""" 
    sql_statement = """SELECT DISTINCT ON (userid) userid, dt_last, total_dist FROM checkpoints ORDER BY userid,total_dist DESC""" 
    checkpoints_most_recent_df = spark.read.format("jdbc").option("url", url).option("user", db_user_name).option("password", db_password).option("driver", "org.postgresql.Driver").option("query", sql_statement).load()
    #checkpoints_most_recent_df.show()
    return checkpoints_most_recent_df

def update_checkpoints_table(checkpoints_new_to_insert_df, url, properties, start_or_update):
    # may need to append .save()
    mode = 'append'
    checkpoints_new_to_insert_df.write.jdbc(url=url, table='checkpoints', mode=mode, properties=properties)
 
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

    schema_type = 'define'
    #schema_type = 'infer'
    if   (schema_type == 'define'):
        # dt,id,lon,lat,hr
        # 0,0,1,0.0,0.0,100
        # 1,566,1,-0.041455384343862534,0.008386597037315369,146
    
        #schema = StructType([
        #    StructField("_c0", IntegerType(),True),
        #    StructField("dt", IntegerType(),True),
        #    StructField("lon", DoubleType(),True),
        #    StructField("lat", DoubleType(),True),
        #    StructField("hr", IntegerType(),True)
        #])
        schema = StructType([
            StructField("_c0", IntegerType()),
            StructField("dt", IntegerType()),
            StructField("id", IntegerType()),
            StructField("lon", DoubleType()),
            StructField("lat", DoubleType()),
            StructField("hr", IntegerType())
        ])        
        #gps_stream_new_df = spark.read.format("csv").schema(schema).option("inferSchema",False).option("header", True).load(file_name_input)
        gps_stream_new_df = spark.read.format("csv").schema(schema).option("header", True).load(file_name_input)
    elif (schema_type == 'infer'):
        gps_stream_new_df = spark.read.format("csv").option("inferSchema",True).option("header", True).load(file_name_input)
        
    print('drop index column')
    gps_stream_new_df = gps_stream_new_df.drop('_c0')
    #print ('showing gps stream csv data')
    #gps_stream_new_df.show()

    # pyspark --packages com.databricks:spark-csv_2.11:1.4.0    
    
    #display(df)
    #print(df.collect())
    #gps_stream_new_df.show()
    #gps_stream_new_df.printSchema()
    
    # csv data example 
    # ,dt,id,lon,lat,hr
    # 0,2000,5509,0.017979517579078674,0.01461024396121502,149
    # 1,2000,37147,0.02834843471646309,-0.017346767708659172,148
    
    print('read csv end ')
    time_end = time.time()
    process_dt_csv_read = (time_end - time_start)/60.0    


    time_start = time.time()
    print('create checkpoints_new_table')
    gps_stream_new_df.createOrReplaceTempView("gps_stream_new_table")

    print('compute difference between points ')
    #df_lon_lat_diff = spark.sql("""SELECT id AS userid, dt, \
    #                               lon, lat, \
    #                               lon-LAG(lon,1,NULL) OVER (PARTITION BY id ORDER BY dt) \
    #                               AS lon_diff, \
    #                               lat-LAG(lat,1,NULL) OVER (PARTITION BY id ORDER BY dt) \
    #                               AS lat_diff \
    #                               FROM gps_stream_new_table
    #                              WHERE id < 5
    #                               ORDER BY id, dt """)

    df_lon_lat_diff = spark.sql("""SELECT id AS userid, dt, \
                                    lon, lat, \
                                    lon-LAG(lon,1,NULL) OVER (PARTITION BY id ORDER BY dt) \
                                    AS lon_diff, \
                                    lat-LAG(lat,1,NULL) OVER (PARTITION BY id ORDER BY dt) \
                                    AS lat_diff \
                                    FROM gps_stream_new_table
                                    ORDER BY id, dt """)
        
    #df_lon_lat_diff.show()
    
    print('create table_lon_lat_diff')    
    df_lon_lat_diff.createOrReplaceTempView("table_lon_lat_diff")
    
    print('compute segment distance and first and last entries in checkpoint ')
    #checkpoints_new_df = spark.sql("""SELECT FIRST(userid) AS userid , \
    #    LAST(dt)   AS   dt_last, \
    #    LAST(lon)  AS  lon_last, \
    #    LAST(lat)  AS  lat_last, \
    #    FIRST(lon) AS lon_first, \
    #    FIRST(lat) AS lat_first, \
    #    100*POWER(POWER(sum(abs(lon_diff)),2)+POWER(sum(abs(lat_diff)),2),0.5) AS segment_dist \
    #    FROM table_lon_lat_diff GROUP BY userid ORDER BY userid""")
    checkpoints_new_df = spark.sql("""SELECT FIRST(userid) AS userid , \
        LAST(dt)/1000.0 AS   dt_last, \
        LAST(lon)  AS  lon_last, \
        LAST(lat)  AS  lat_last, \
        FIRST(lon) AS lon_first, \
        FIRST(lat) AS lat_first, \
        10*POWER(POWER(sum(abs(lon_diff)),2)+POWER(sum(abs(lat_diff)),2),0.5) AS segment_dist \
        FROM table_lon_lat_diff GROUP BY userid ORDER BY userid""")

    if (show_tables):
        print ('showing checkpoints_new')
        checkpoints_new_df.show()

    print('create table_checkpoints_new')    
    checkpoints_new_df.createOrReplaceTempView("table_checkpoints_new")
        
    #qc_large_segments = True                  
    #if (qc_large_segments):
    #    sql_statement = """UPDATE table_checkpoints_new SET segment_dist = NULL WHERE segment_dist > 50.0""";
    #    cursor.execute(sql_statement)
      
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

    time_end = time.time()
    process_dt_join_tables = (time_end - time_start)/60.0    

    time_start = time.time()

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
    print('#################################################')
    print('file_name_input  is %s' %(file_name_input))
    print (f'csv_read                took {process_dt_csv_read :6.2f} minutes ')
    print (f'process_new             took {process_dt_process_new_checkpoints  :6.2f} minutes ')
    print (f'read_old_checkpoints    took {process_dt_read_old_checkpoints:6.2f} minutes ')
    print (f'read_checkpoints_recent took {process_dt_read_checkpoints_most_recent:6.2f} minutes ')
    print (f'join_tables             took {process_dt_join_tables:6.2f} minutes ')
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
        print('start_or_update is %s' %(start_or_update))
        print('calling main before ')
        main(file_name_input, file_name_output, start_or_update)
        print('script executed succesfully ')
        print('script executed succesfully ')


# alternative read syntax 
#checkpoints_most_recent_df = spark.read\
#    .format("jdbc") \
#    .option("url", url) \
#    .option("user",     os.environ['db_user_name']) \
#    .option("password", os.environ['db_password']) \
#    .option("driver", "org.postgresql.Driver")\
#    .option("query", sql_statement)\
#    .load()
#    .option("dbtable",  "checkpoints") \

# alternative update_checkpoints_table syntax
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


