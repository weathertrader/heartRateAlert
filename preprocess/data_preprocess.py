# data_preprocess.py 
# reads in raw gps data and write a csv ordered by timestamp 
# usage: 
# python data_preprocess.py data_subset_proper.json processed_data.csv

import os
#import ast
#import json
#import datetime as dt
from datetime import datetime as dt
import random
import pandas as pd
import numpy as np
import sys
#import csv
import time

# flags to aid in manual debugging inside and IDE/Ipython console
#manual_debug = True
#manual_debug = False

def preprocess_inputs(input_file, output_file):
    
    # print ('setting input and output file names ')
    # if (manual_debug): # manually set input and output files for debugging in Ipython or IDE
    #     base_dir = os.getcwd()
    #     base_dir = '/home/craigmatthewsmith/consumer_complaints_cs'
    #     os.chdir(base_dir)
    #     input_file  = os.path.join(base_dir,'input','consumer_complaints.csv')
    #     output_file = os.path.join(base_dir,'output','report.csv')
    # else:
    #     input_file  = sys.argv[1]
    #     output_file = sys.argv[2]
    # print('using input  file %s ' %(input_file))
    # print('using output file %s ' %(output_file))

    #dir_work = '/home/craigmatthewsmith/heartRateAlert'
    # os.chdir(dir_work)
    dir_work = os.getcwd()
    print('working directory is %s ' %(os.getcwd()))
    #dir_data = os.path.join(dir_work, 'data')
    #print(os.path.isdir(dir_data))

    #file_name_data = os.path.join(dir_data, 'data_subset_proper.json')
    #os.path.isfile(file_name_data)
    data = []
    #with gzip.open(input_file) as f:
    #with open(os.path.join('endomondoHR_proper.json')) as f:
    with open(input_file) as f:
        for l in f:
            data.append(eval(l))

    # add random noise to start of tracks
    dt_offset_scaling = 10.0
    lon_offset_scaling = 1.0
    lat_offset_scaling = 1.0
        
    lon_all   = []
    lat_all   = []
    dt_all    = []
    user_all  = []
    
    n_activities = len(data)
    #n_activities = 10
    f = 0
    for f in range(0, n_activities, 1):
        dt_offset_temp = int(dt_offset_scaling*random.random())
        lon_offset_temp = lon_offset_scaling*(random.random()-1.0)
        lat_offset_temp = lat_offset_scaling*(random.random()-1.0)
        data_temp = data[f]
        n_records = len(data_temp['longitude'])
        #n_records = 10
        print ('  processing activity %s of %s with %s n_records and offsets dt %3.0f, lon %5.2f, lat %5.2f ' %(f, n_activities, n_records, dt_offset_temp, lon_offset_temp, lat_offset_temp))
        #print ('  dt min - max is %s - %s ' %(data_temp['timestamp'][0], data_temp['timestamp'][-1] - data_temp['timestamp'][0]))
        #try: 
        #    speed_all.append(data_temp['speed'])
        #except: 
        #    print('f %s mising speed data'%(f))
        #lon_all.append(list(np.array(data_temp['longitude'][0:n_records]) - data_temp['longitude'][0] + lon_offset_temp))
        #lat_all.append(list(np.array(data_temp['latitude'][0:n_records]) - data_temp['latitude'][0] + lat_offset_temp))
        #lat_all.append(list(np.array(data_temp['latitude'][0:n_records)) - data_temp['latitude'][0] + lat_offset_temp))
        #dt_all.append( list(np.array(data_temp['timestamp'][0:n_records]) - data_temp['timestamp'][0] +  dt_offset_temp))
        for n in range(0, n_records, 1):
            #user_all.append(data_temp['id'])
            user_all.append(f+1)
            lon_all.append(data_temp['longitude'][n] - data_temp['longitude'][0] + lon_offset_temp)
            lat_all.append(data_temp[ 'latitude'][n] - data_temp[ 'latitude'][0] + lat_offset_temp)
            #lat_all.append(list(np.array(data_temp['latitude'][0:n_records)) - data_temp['latitude'][0] + lat_offset_temp))
            dt_all.append( data_temp['timestamp'][n] - data_temp['timestamp'][0] +  dt_offset_temp)
    
    # print min and max values 
    print ('dt   min - max is %5.0f - %5.0f' %(np.nanmin(dt_all), np.nanmax(dt_all)))
    print ('user min - max is %5.0f - %5.0f' %(np.nanmin(user_all), np.nanmax(user_all)))
    print ('lon  min - max is %5.2f - %5.2f' %(np.nanmin(lon_all), np.nanmax(lon_all)))
    print ('lat  min - max is %5.2f - %5.2f' %(np.nanmin(lat_all), np.nanmax(lat_all)))
        
    # zero out dt, lon and lat
    lon_all = list(np.array(lon_all) - min(lon_all))
    lat_all = list(np.array(lat_all) - min(lat_all))
    dt_all  = list(np.array( dt_all) - min( dt_all))
    
    print ('lon  min - max is %5.2f - %5.2f' %(np.nanmin(lon_all), np.nanmax(lon_all)))
    print ('lat  min - max is %5.2f - %5.2f' %(np.nanmin(lat_all), np.nanmax(lat_all)))
    
    column_str = ['dt', 'user', 'lon', 'lat']
    data_array = np.array([dt_all, user_all, lon_all, lat_all]).T
    data_df = pd.DataFrame (data_array, columns=column_str)
    #data_df.sort_values(by=['dt', 'user'])
    data_df = data_df.sort_values(by=['dt', 'user'])
    processed_data_file_name = os.path.join(dir_work,'processed_data.csv')
    print      ('processed_data_file_name is %s ' %(processed_data_file_name))
    data_df.to_csv(processed_data_file_name) 
    data_df.head(40)
    
    #lon_all
    #lat_all
    
    #dt_all
    #len(user_all)
    #len(set(user_all))
    
if __name__ == '__main__':
    input_file  = sys.argv[1]
    output_file = sys.argv[2]
    print('using input  file %s ' %(input_file))
    print('using output file %s ' %(output_file))
    preprocess_inputs(input_file, output_file)



# yy_recvd_list = []
# product_list  = []
# company_list  = []
# with open(input_file, "r", encoding="utf-8") as csv_read_file: # force utf-8 encoding 
#     next(csv_read_file)
#     for row in csv.reader(csv_read_file):
#         # here check number of entries per row
#         n_fields = len(row)
#         #print ('%s n_fields found' %(n_fields))
#         if not (n_fields == n_fields_expected):
#             print ('ERROR - incorrect number of fields in row %s ' %(row))
#         else: 
#             dt_temp_str =  row[0]
#             product_temp = row[1]
#             company_temp = row[7]
#             if (str.isspace(product_temp) or str.isspace(company_temp) or not(product_temp) or not(company_temp)):
#                 print ('ERROR with product or company fields, "%s", "%s" ' %(product_temp, company_temp))
#                 next(csv_read_file)
#             else: # continue reading this row 
#                 try: # if any single one fails, no fields should be appended at all 
#                     #yy_recvd_list.append(dt.datetime.strptime(dt_temp_str, '%Y-%m-%d').year)
#                     yy_recvd_list.append(dt.datetime.strptime(dt_temp_str, '%Y-%m-%d').year)
#                     product_list.append(product_temp.lower())
#                     company_list.append(company_temp.lower())
#                 except: # ValueError: 
#                     print ('ERROR skipping row  due to malformed datet






    