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
else:
    work_dir = os.getcwd()
# work_dir = os.path.join(base_dir, 'raceCast')

#print(os.environ.get('db_name'))
#print(os.environ['db_name'])


###############################################################################
###############################################################################
# read from pg 

from pyspark.sql import SQLContext
from pyspark.sql import SparkSession

# submit from cli
.\bin\spark-shell --packages org.postgresql:postgresql:42.1.1
--jars /path/to/driver/postgresql-42.2.1.jar    

# jars
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.postgresql:postgresql:42.1.1 pyspark-shell'
os.environ['PYSPARK_SUBMIT_ARGS'] = '--jars file:///D:/sqlite-jdbc-3.23.1.jar pyspark-shell'
spark = SparkSession.builder.config('spark.driver.extraClassPath', '/path/to/postgresql.jar').getOrCreate()

# connect

url = 'jdbc:postgresql://'+os.environ['db_host']+':'+os.environ['db_port']+'/'+os.environ['db_name']
print('url is %s' %(url))

sc = SparkContext(conf=conf)
sqlContext = SQLContext(sc)

# driver may not be needed
properties = {
    'user': os.environ['db_user_name'],
    'password': os.environ['db_password'],
    'driver': "org.postgresql.Driver",
}

# read
df =      spark.read.jdbc(url=url, table='checkpoints', properties=properties)
df = sqlContext.read.jdbc(url=url, table='checkpoints', properties=properties) 


# write
df.write.jdbc(url=url, table="baz", mode=mode, properties=properties)




def read_postgres():
    df = spark.read\
        .format("jdbc") \
        .option("url", url) \
        .option("user", user) \
        .option("password", password) \
        .option("dbtable", "pages") \
        .load()



def get_value_from_psql(value, table_name):
	query = "select "+ value + " from " + table_name
	out= spark.read \
	.format("jdbc") \
	.option("url", "jdbc:postgresql://10.0.0.9:5432/"+os.environ['PSQL_DB']) \
    .option("user", os.environ['PSQL_UNAME']) \
    .option("driver", "org.postgresql.Driver")\
    .option("password",os.environ['PSQL_PWD'])\
    .option("query", query)\
    .load()
	return out

def write_to_postgres(pages_in_out):
    pages_in_out.select('page_id', 'page_title', 'time_stamp', 'links', 'link_cnt', 'count').\
        write.jdbc(url=url,
                   table='pages_in_out',
                   properties=properties,
                   mode='append')

    print("POSTGRES DONE")

def write_to_psql(df, table_name, action):
	df.write \
    .format("jdbc") \
    .mode(action)\
    .option("url", "jdbc:postgresql://10.0.0.9:5432/"+os.environ['PSQL_DB']) \
    .option("dbtable", table_name) \
    .option("user", os.environ['PSQL_UNAME']) \
    .option("driver", "org.postgresql.Driver")\
    .option("password",os.environ['PSQL_PWD'])\
    .save()

def insertSql(df):
    df.write.format("jdbc")\
            .option("url", "jdbc:mysql://" + sql_host + "/airplanes")\
            .option("dbtable", "planes")\
            .option("driver", "com.mysql.cj.jdbc.Driver")\
            .option("user", sql_username)\
            .option("password", sql_password).mode("append").save()

###############################################################################
###############################################################################




def main(file_name_input, file_name_output):
    
    time_start_all = time.time()
    time_start_read = time.time()
    
    print('start spark session ')
    spark = SparkSession\
        .builder\
        .appName("batch_process_gps")\
        .getOrCreate()

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
    
    # df = spark.read.format("csv").schema(schema).option("header",True).load(file_name_input)
    # df = spark.read.format("com.databricks.spark.csv").schema(schema).option("header",True).load(file_name_input)
    
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

    print('sql select ')
    df_lon_lat_diff = spark.sql("""SELECT id AS id, dt, \
                               lon, lat, \
                               lon-LAG(lon,1,NULL) OVER (PARTITION BY id ORDER BY dt) \
                               AS lon_diff, \
                               lat-LAG(lat,1,NULL) OVER (PARTITION BY id ORDER BY dt) \
                               AS lat_diff \
                               FROM table_read""")

    #df_lon_lat_diff.show()

    print('create table_lon_lat_diff')    
    df_lon_lat_diff.createOrReplaceTempView("table_lon_lat_diff")
    

    print('sql select ')
    df_lon_lat_sum = spark.sql("""SELECT id, \
                              sum(abs(lon_diff)) as sum_lon_diff, \
                              sum(abs(lat_diff)) as sum_lat_diff \
                              FROM table_lon_lat_diff GROUP BY (id) \
                              """)

    #df_lon_lat_sum.show()

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

    # print timing to console 
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

    
    