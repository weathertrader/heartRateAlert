# create_db.py 
# purpose - create tables for the gps data 
# usage on pg_server 
# python3 src/create_db.py

# usage - python3 src/update_db.py data/gps_batch_1.csv update


import os
import sys
import psycopg2

def main():

    print('using the following environmental variables from .bashrc ')    
    print('  db_name      %s ' %(os.environ['db_name']))
    print('  db_host      %s ' %(os.environ['db_host']))
    print('  db_user_name %s ' %(os.environ['db_user_name']))
    print('  db_port      %s ' %(os.environ['db_port']))
        
    print('open_connection_to_db ')    
    try:
        conn = psycopg2.connect(database = os.environ['db_name'], 
                                host     = os.environ['db_host'], 
                                user     = os.environ['db_user_name'], 
                                password = os.environ['db_password'], 
                                port     = os.environ['db_port'])    
        autocommit = True
        if (autocommit):
            conn.autocommit = True
        cursor = conn.cursor()
        print('open_connection_to_db success ') 
    except:
        print('open_connection_to_db: ERROR ') 
        sys.exit()

    try:
        sql_statement = """DROP TABLE leaderboard;"""
        cursor.execute(sql_statement)
    except psycopg2.ProgrammingError:
        print      ('ERROR - table does not exist ') 

    #sql_statement = """CREATE TABLE leaderboard (
    #                    userid     INT PRIMARY KEY,
    #                    dt_last    FLOAT  NOT NULL,
    #                    lon_last   FLOAT  NOT NULL, 
    #                    lat_last   DOUBLE PRECISION  NOT NULL, 
    #                   total_dist FLOAT  NOT NULL
    #                    );"""
    sql_statement = """CREATE TABLE leaderboard (
                        userid     INT,
                        dt_last    FLOAT  NOT NULL,
                        lon_last   FLOAT  NOT NULL, 
                        lat_last   DOUBLE PRECISION  NOT NULL, 
                        total_dist FLOAT  NOT NULL,
                        PRIMARY KEY (userid)                       
                        );"""
    #print(sql_statement)
    cursor.execute(sql_statement)

    print('table leaderboard successfully created')

    try:
        sql_statement = """DROP TABLE checkpoints;"""
        cursor.execute(sql_statement)
    except psycopg2.ProgrammingError:
        print      ('ERROR - table does not exist ') 
 
    sql_statement = """CREATE TABLE checkpoints (
                       userid       INT,
                       dt_last      FLOAT,
                       lon_last     FLOAT  NOT NULL, 
                       lat_last     DOUBLE PRECISION  NOT NULL, 
                       segment_dist FLOAT  NOT NULL,
                       total_dist   FLOAT  NOT NULL,
                       PRIMARY KEY (userid, dt_last)
                       );"""
    #print(sql_statement)
    cursor.execute(sql_statement)    
    print('table checkpoints successfully created')
        
    #delete_all_entries_from_table = True
    #delete_all_entries_from_table = False
    #if (delete_all_entries_from_table):
    #    sql_statement = """DELETE FROM leaderboard;"""
    #    cursor.execute(sql_statement)
    #    sql_statement = """DELETE FROM checkpoints;"""
    #    cursor.execute(sql_statement)
      
if __name__ == "__main__":
    print('creating new tables')
    main()
    print('tables successfully created')
