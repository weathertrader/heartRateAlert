# update_db.py 
# purpose - update tables with latest batch results
# usage - python3 src/update_db.py data/gps_batch_0.csv start
# usage - python3 src/update_db.py data/gps_batch_1.csv update

# done
#       read csv batch processing results 
#       connect to db on local
#       create table if not exists
#       insert into table 
#       read table 
#       read table, add csv, update table
#       create config file and add to .bashrc
#       run from pg w/ data on pg
#       read csv from s3 from local and pg
#       update db from local to local
#       update db from aws pg to aws pg  

# 1 hr  read s3 hosted csv from master and worker; sudo apt-get install s3fs

# 2 hr  update db from  local to aws pg
# 2 hr  update db from master to aws pg
# 2 hr  update db from worker to aws pg

# timing 
# bulk insert 

import os
import sys
import numpy as np
#from operator import add
#from functools import reduce
#import csv
import time
import pandas as pd
import psycopg2
import s3fs

#host_name = 'local'
#host_name = 'master'
host_name = 'pg'
#batch_num = 0
batch_num = 1
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
    work_dir = os.path.join(base_dir, 'heartRateAlert')
    os.chdir(work_dir)
else:
    work_dir = os.getcwd()

#print(os.environ.get('db_name'))
#print(os.environ['db_name'])


def main(file_name_input, drop_and_create_table):

    print('open_connection_to_db ')    
    try:
        connection = psycopg2.connect(database = os.environ['db_name'], 
                                      host     = os.environ['db_host'], 
                                      user     = os.environ['db_user_name'], 
                                      password = os.environ['db_password'], 
                                      port     = os.environ['db_port'])    
        autocommit = True
        if (autocommit):
            connection.autocommit = True
        cursor = connection.cursor()
        print      ('open_connection_to_db success ') 
    except:
        print      ('open_connection_to_db: ERROR ') 
        
    #drop_and_create_table = False
    print('drop_and_create_table is %s' %(drop_and_create_table))    
    if (drop_and_create_table):
        sql_statement = """DROP TABLE leaderboard;"""
        cursor.execute(sql_statement)
        # should dt be a primary key as well 
        sql_statement = """CREATE TABLE leaderboard (
                            userid     INT PRIMARY KEY,
                            dt         FLOAT  NOT NULL,
                            lon_last   FLOAT  NOT NULL, 
                            lat_last   DOUBLE PRECISION  NOT NULL, 
                            total_dist FLOAT  NOT NULL
                            );"""
        #print(sql_statement)
        cursor.execute(sql_statement)
    
        print('table dropped and created sucessfully ')
        
    #delete_all_entries_from_table = True
    delete_all_entries_from_table = False
    if (delete_all_entries_from_table):
        sql_statement = """DELETE FROM leaderboard;"""
        cursor.execute(sql_statement)
        
    #batch_num = 0
    #for batch_num in range(0, 4, 1):
    #    print('  processing batch_num %s' %(batch_num))
    
    time_start = time.time()
    
    #file_name_input  = os.path.join(work_dir, 'data', 'gps_batch_'+str(batch_num)+'.csv')
    #file_name_input  = 's3a://gps-data-processed/gps_batch_' +str(batch_num)+'.csv'        
    print('using input file %s ' %(file_name_input))
    if not (file_name_input.startswith('s3')):
        if not (os.path.isfile(file_name_input)):
            print('ERROR - missing input file')
            sys.exit('ERROR - missing input file')

    print('reading input file')
    batch_df = pd.read_csv(file_name_input,index_col=0)
    #print(batch_df.head())
    # stn_read_df_matrix = stn_read_csv.as_matrix()
    # list(batch_df)
    total_dist = np.sqrt(batch_df['lon_last']**2.0 + batch_df['lat_last']**2.0)
 
    time_end = time.time()
    process_dt = (time_end - time_start)/60.0
    print ('read_data took %5.2f minutes ' %(process_dt))
    
    time_start = time.time()
    
    n_ids = len(batch_df)
    n = 0
    #for n in range(0, 1, 1):    
    for n in range(0, n_ids, 1):    
        print('  processing user %5.0f of %5.0f ' %(n, n_ids))
        sql_statement = """SELECT userid, dt, lon_last, lat_last, total_dist FROM leaderboard WHERE userid = '%s'""" % (int(batch_df['id'][n]))
        cursor.execute(sql_statement)
        results = cursor.fetchall()
        if   (len(results) == 0):
            total_dist_new = total_dist[n]
            print('    no entries found')
        elif (len(results) > 0):
            #print(results)
            [userid_prev, dt_prev, lon_last_prev, lat_last_prev, total_dist_prev] = results[0]
            print('    found user %s dt %5.1f lon %5.1f lat %5.1f  dist %5.1f ' %(userid_prev, dt_prev, lon_last_prev, lat_last_prev, total_dist_prev))
            lon_diff = np.abs(batch_df['lon_first'][n] - lon_last_prev)
            lat_diff = np.abs(batch_df['lat_first'][n] - lat_last_prev)
            total_dist_inc = np.sqrt(lon_diff**2.0 + lat_diff**2.0)
            total_dist_new = total_dist_prev + total_dist[n] + total_dist_inc
            print('    total_dist new %5.2f, prev %5.2f, current %5.2f, inc %5.2f ' %(total_dist_new, total_dist_prev, total_dist[n], total_dist_inc))
            
        # no update
        #sql_statement = """INSERT INTO leaderboard
        #          (                userid,                     dt,                lon_last,                lat_last,     total_dist) 
        #    VALUES(                    %s,                     %s,                      %s,                      %s,             %s)""" \
        #        % (int(batch_df['id'][n]), batch_df['dt_last'][n], batch_df['lon_last'][n], batch_df['lat_last'][n], total_dist_new)
        # with update
        # cursor.execute(sql_statement)
        # UPDATE table_name SET column1 = value1, column2 = value2, ... WHERE condition;
        cursor.execute("""INSERT INTO leaderboard 
            (userid, dt, lon_last, lat_last, total_dist) 
            VALUES( %s, %s, %s, %s, %s)""" \
            % (int(batch_df['id'][n]), batch_df['dt_last'][n], batch_df['lon_last'][n], batch_df['lat_last'][n], total_dist_new) \
            +""" ON CONFLICT(userid) DO UPDATE SET 
            (dt, lon_last, lat_last, total_dist) = 
            (EXCLUDED.dt, EXCLUDED.lon_last, EXCLUDED.lat_last, EXCLUDED.total_dist)""")
 
    print('data successfully inserted to db ')
    time_end = time.time()
    process_dt = (time_end - time_start)/60.0
    print ('insert data took %5.2f minutes ' %(process_dt))
        

if __name__ == "__main__":
    if (len(sys.argv) != 3):
        print("Usage: python3 update_db.py <file> <start/update>", file=sys.stderr)
        sys.exit(-1)
    else:
        file_name_input = sys.argv[1]        
        start_or_update = sys.argv[2]        
        print('start_or_update is %s' %(start_or_update))
        if   (start_or_update == 'start'):
            drop_and_create_table = True
        elif (start_or_update == 'update'):
            drop_and_create_table = False
        else:
            print('ERROR - only start or update accepted as cli')
            sys.exit()
        print('drop_and_create_table is %s' %(drop_and_create_table))
        print('calling main before ')
        main(file_name_input, drop_and_create_table)
        print('script executed succesfully ')


# cursor.execute("""SELECT datetime_valid, u_ws, v_ws FROM wrf 
#                WHERE stn_id='%s' AND 
#                hgt='%s' AND 
#                domain=3 AND 
#                ensemble_member='acm2_px' AND 
#                datetime_init = '%s' AND 
#                datetime_valid >= '%s' AND 
#                datetime_valid <= '%s'""" 
#                % (stn_id[s], 
#                   dict_post_process_options['extract_profile_hgts'][h], 
#                   datetime_init, 
#                   datetime_start_temp, 
#                   datetime_end_temp))

#cursor.execute(sql_statement)
#results = cursor.fetchall()
#print(results)

#print      ('    found %s results ' % (len(results)))
#logger.info('    found %s results ' % (len(results)))

# ['id','dt_first','dt_last','sum_lon_diff','sum_lat_diff','lon_first','lon_last','lat_first','lat_last']

# sql_statement = """CREATE TABLE stn_metadata(
#               id          TEXT NOT NULL PRIMARY KEY,
#               name        TEXT NOT NULL,
#               stn_obs_hgt FLOAT NOT NULL DEFAULT 10.0,
#               mnet_id     INT4,
#               lon         DOUBLE PRECISION,
#               lat         DOUBLE PRECISION,
#               elev        FLOAT
#               )"""


#sql_statement = 'CREATE TABLE obs_ws(datetime_valid  TIMESTAMP, '+stn_list_srt+',  PRIMARY KEY (datetime_valid))' 
#print(sql_statement)
#cursor.execute(sql_statement)

#try:
#    cursor.execute("""DROP TABLE stn_metadata""")
#except psycopg2.ProgrammingError:
#    print      ('ERROR - table does not exist ') 

# cursor.execute("""CREATE TABLE stn_metadata(
#               id          TEXT NOT NULL PRIMARY KEY,
#               name        TEXT NOT NULL,
#               stn_obs_hgt FLOAT NOT NULL DEFAULT 10.0,
#               mnet_id     INT4,
#               lon         DOUBLE PRECISION,
#               lat         DOUBLE PRECISION,
#               elev        FLOAT
#               )""")

# cursor.execute("""CREATE TABLE IF NOT EXISTS """+table_name+"""(
#            datetime_valid TIMESTAMP WITH TIME ZONE,
#            stn_id  TEXT NOT NULL,
#            hgt     DOUBLE PRECISION,
#            ws      DOUBLE PRECISION,
#            wd      DOUBLE PRECISION,
#            u_ws    DOUBLE PRECISION,
#            v_ws    DOUBLE PRECISION,
#            temp    DOUBLE PRECISION,
#            rh      DOUBLE PRECISION,
#            PRIMARY KEY(datetime_valid, stn_id)
#           )""")    
    

    

