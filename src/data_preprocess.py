# data_preprocess.py 
# reads in raw gps data and write a csv ordered by timestamp 
# usage: 
# python preprocess/data_preprocess.py data/endomondoHR_proper.json processed_data.csv
# python preprocess/data_preprocess.py data/gps_tracks_0.txt gps_tracks_processed_0.csv
# split -l 20000 endomondoHR_proper.json
# mv xaa gps_data_0.csv 

import os
import ast
#import json
#import datetime as dt
from datetime import datetime as dt
import random
import pandas as pd
import numpy as np
import sys
#import csv
import time



# debugging 
#input_file = 'data/endomondoHR_proper.json'
#input_file = 'data/data_subset_proper.json'
# input_file = 'data/gps_tracks_0.txt'
#output_file = 'processed_data_0.csv'
#dir_work = '/home/craigmatthewsmith/heartRateAlert'
#os.chdir(dir_work)


# flags to aid in manual debugging inside and IDE/Ipython console
# manual_debug = True
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

    #dir_work = os.getcwd()
    #print('working directory is %s ' %(os.getcwd()))
    #dir_data = os.path.join(dir_work, 'data')
    #print(os.path.isdir(dir_data))

    print('file read begin ')

    #file_name_data = os.path.join(dir_data, 'data_subset_proper.json')
    #os.path.isfile(file_name_data)
    #data = []
    #with open(input_file) as file_open:
    #    for line in file_open:
    #        data.append(eval(l))
            
    # add random noise to start of tracks
    dt_offset_scaling  = 10.0
    lon_offset_scaling = 1.0
    lat_offset_scaling = 1.0

    n_records = 500
    #n_activities = 168000
    # 83892000
    # chokes 
    n_activities = 20000
    
    #n_subset = int(168000/n_activities)+1

    #subset = 5
    #for subset in range(4, n_subset, 1):
    count = 0
    line_count = 0
    #start_count = subset*n_activities
    #end_count = start_count + n_activities
    #print ('  subset %6.0f of %6.0f, start_count %6.0f, end_count %6.0f ' %(subset, n_subset, start_count, end_count))
 
    time_start = time.time()
    print ('read data ')
 
    #data_all   = np.full([n_activities*n_records,4], np.nan, dtype=float)
    lon_all   = np.full([n_activities*n_records], np.nan, dtype=float)
    lat_all   = np.full([n_activities*n_records], np.nan, dtype=float)
    dt_all    = np.full([n_activities*n_records], 0, dtype=int)
    user_all  = np.full([n_activities*n_records], 0, dtype=int)
               
    print('input file open')
    with open(input_file) as file_open:
        for line in file_open:
            #if (line_count%100 == 0):
            #    #print ('    count %6.0f line_count %6.0f with %3.0f n_records and offsets dt %3.0f, lon %5.2f, lat %5.2f ' %(count, line_count, n_records, dt_offset_temp, lon_offset_temp, lat_offset_temp))
            #    print ('      line_count %6.0f start_count %6.0f end_count %6.0f ' %(line_count, start_count, end_count))
            #if (line_count < start_count):
            #    next(file_open)
            #if (count < n_activities):
            #elif (line_count >= start_count and line_count < end_count):
            # can skip lines using 
            #next(f)
            dt_offset_temp = int(dt_offset_scaling*random.random())
            #dt_offset_temp = float(dt_offset_scaling*random.random())
            lon_offset_temp = lon_offset_scaling*(random.random()-1.0)
            lat_offset_temp = lat_offset_scaling*(random.random()-1.0)
            #file_line_temp = "{'longitude': [24.64977040886879, 24.65014273300767,  24.368406180292368, 24.6496663056314], 'altitude': [41.6, 40.6, 40.6, 38.4], 'latitude': [60.173348765820265, 60.173239801079035, 60.17298021353781, 60.17335429787636], 'sport': 'bike', 'id': 396826535, 'heart_rate': [100, 111, 120, 119], 'gender': 'male', 'timestamp': [1408898746, 1408898754, 1408898765, 1408898778], 'url': 'https://www.endomondo.com/users/10921915/workouts/396826535','userId': 10921915, 'speed': [6.8652, 16.4736, 19.1988, 20.4804]}"        
            #line_strip = file_line_temp.replace(':','').replace('{','').replace('}','')
            #line_strip = file_lines[f].replace(':','').replace('{','').replace('}','')        
            line_strip = line.replace(':','').replace('{','').replace('}','')        
            lon_temp = np.array(ast.literal_eval(line_strip.split('longitude')[1].split('altitude')[0].replace('],',']').replace("' ",'').replace("] '",']')))
            lat_temp = np.array(ast.literal_eval(line_strip.split('latitude')[1].split('sport')[0].replace('],',']').replace("' ",'').replace("] '",']')))
            dt_temp  = np.array(ast.literal_eval(line_strip.split('timestamp')[1].split('url')[0].replace('],',']').replace("' ",'').replace("] '",']')))
            #lon_temp = np.array(lon_temp)
            #lat_temp = np.array(lat_temp) 
            #dt_temp  = np.array( dt_temp) 
            lon_temp = lon_temp - lon_temp[0]
            lat_temp = lat_temp - lat_temp[0] 
            dt_temp  =  dt_temp -  dt_temp[0] 
            lon_temp = lon_temp + lon_offset_temp
            lat_temp = lat_temp + lat_offset_temp
            dt_temp  =  dt_temp +  dt_offset_temp

            #n_records = len(lon_temp)
            #n_records = 10
            if (count%1000 == 0):
                #print ('    count %6.0f line_count %6.0f with %3.0f n_records and offsets dt %3.0f, lon %5.2f, lat %5.2f ' %(count, line_count, n_records, dt_offset_temp, lon_offset_temp, lat_offset_temp))
                print ('  count %6.0f line_count %6.0f dt min max is %6.0f %6.0f ' %(count, line_count, dt_temp[0], dt_temp[-1]))

            #data_all[(count*n_records):(count*n_records+n_records),0] =  dt_temp
            #data_all[(count*n_records):(count*n_records+n_records),1] = line_count+1
            #data_all[(count*n_records):(count*n_records+n_records),2] = lon_temp
            #data_all[(count*n_records):(count*n_records+n_records),3] = lat_temp
            dt_all  [(count*n_records):(count*n_records+n_records)] =  dt_temp
            user_all[(count*n_records):(count*n_records+n_records)] = count+1
            lon_all [(count*n_records):(count*n_records+n_records)] = lon_temp
            lat_all [(count*n_records):(count*n_records+n_records)] = lat_temp
            count += 1
        #line_count += 1
    
    time_end = time.time()
    process_dt = (time_end - time_start)/60.0
    # takes 10 min
    print ('read data took %5.2f minutes ' %(process_dt))
                
    print('file read end ')

    print('truncate arrays ')
    #data_all = data_all[0:(count*n_records),:]
    user_all = user_all[0:(count*n_records+n_records)]
    lon_all  =  lon_all[0:(count*n_records+n_records)]
    lat_all  =  lat_all[0:(count*n_records+n_records)]
    dt_all   =   dt_all[0:(count*n_records+n_records)]
    
    # print min and max values 
    #print ('dt   min - max is %5.0f - %5.0f' %(np.nanmin(data_all[:,0]), np.nanmax(data_all[:,0])))
    #print ('user min - max is %5.0f - %5.0f' %(np.nanmin(data_all[:,1]), np.nanmax(data_all[:,1])))
    #print ('lon  min - max is %5.2f - %5.2f' %(np.nanmin(data_all[:,2]), np.nanmax(data_all[:,2])))
    #print ('lat  min - max is %5.2f - %5.2f' %(np.nanmin(data_all[:,3]), np.nanmax(data_all[:,3])))
    print ('user min - max is %5.0f - %5.0f' %(np.nanmin(user_all), np.nanmax(user_all)))
    print ('dt   min - max is %5.0f - %5.0f' %(np.nanmin(  dt_all), np.nanmax(  dt_all)))
    print ('lon  min - max is %5.2f - %5.2f' %(np.nanmin( lon_all), np.nanmax( lon_all)))
    print ('lat  min - max is %5.2f - %5.2f' %(np.nanmin( lat_all), np.nanmax( lat_all)))
        
    # zero out dt, lon, and lat
    #data_all[:,0] = data_all[:,0] - np.nanmin(data_all[:,0])
    #data_all[:,2] = data_all[:,2] - np.nanmin(data_all[:,2])
    #data_all[:,3] = data_all[:,3] - np.nanmin(data_all[:,3])
    lon_all = lon_all - np.nanmin(lon_all)
    lat_all = lat_all - np.nanmin(lat_all)
    dt_all  =  dt_all - np.nanmin( dt_all)

    #print ('dt   min - max is %5.0f - %5.0f' %(np.nanmin(data_all[:,0]), np.nanmax(data_all[:,0])))
    #print ('user min - max is %5.0f - %5.0f' %(np.nanmin(data_all[:,1]), np.nanmax(data_all[:,1])))
    #print ('lon  min - max is %5.2f - %5.2f' %(np.nanmin(data_all[:,2]), np.nanmax(data_all[:,2])))
    #print ('lat  min - max is %5.2f - %5.2f' %(np.nanmin(data_all[:,3]), np.nanmax(data_all[:,3])))
    
    print ('user min - max is %5.0f - %5.0f' %(np.nanmin(user_all), np.nanmax(user_all)))
    print ('dt   min - max is %5.0f - %5.0f' %(np.nanmin(  dt_all), np.nanmax(  dt_all)))
    print ('lon  min - max is %5.2f - %5.2f' %(np.nanmin( lon_all), np.nanmax( lon_all)))
    print ('lat  min - max is %5.2f - %5.2f' %(np.nanmin( lat_all), np.nanmax( lat_all)))
    
    index_sort = np.argsort(dt_all)
    data_all = np.array([dt_all[index_sort], user_all[index_sort], lon_all[index_sort], lat_all[index_sort]]).T
    
    del dt_all, user_all, lon_all, lat_all

    #data_array = np.stack([dt_all, user_all, lon_all, lat_all], axis=0) # .T
    # del dt_all, user_all, lon_all, lat_all

    column_str = ['dt', 'user', 'lon', 'lat']
    #data_df = pd.DataFrame (data_array, columns=column_str)
    #data_df = pd.DataFrame (data_all.T, columns=column_str)
    data_df = pd.DataFrame (data_all, columns=column_str)
    del data_all
    #data_df.sort_values(by=['dt', 'user'])
    #data_df = data_df.sort_values(by=['dt', 'user'])
    print('    sort df start ')
    data_df = data_df.sort_values(by=['dt'])
    print('    sort df end ')
    #processed_data_file_name = os.path.join(dir_work,'processed_data.csv')
    #processed_data_file_name = os.path.join(dir_work,'processed_data_subset_'+str(subset)+'.csv')
    #print('    processed_data_file_name is %s ' %(processed_data_file_name))
    #data_df.to_csv(processed_data_file_name) 
    print('output_file is %s ' %(output_file))
    data_df.to_csv(output_file) 
    #data_df.head(40)

if __name__ == '__main__':
    input_file  = sys.argv[1]
    output_file = sys.argv[2]
    print('using input  file %s ' %(input_file))
    print('using output file %s ' %(output_file))
    preprocess_inputs(input_file, output_file)


# input_file_open = open(input_file,'r')
# print('input file open')
# file_lines = input_file_open.readlines()
# n_lines = len(file_lines)
# print('found %s lines' %(n_lines))
# f = 6 
# for f in range(0, n_lines, 1): 
#     line = file_lines[f]
#     dt_offset_temp = int(dt_offset_scaling*random.random())
#     lon_offset_temp = lon_offset_scaling*(random.random()-1.0)
#     lat_offset_temp = lat_offset_scaling*(random.random()-1.0)

#     line_strip = line.replace(':','').replace('{','').replace('}','')        
#     lon_temp = np.array(ast.literal_eval(line_strip.split('longitude')[1].split('altitude')[0].replace('],',']').replace("' ",'').replace("] '",']')))
#     lat_temp = np.array(ast.literal_eval(line_strip.split('latitude')[1].split('sport')[0].replace('],',']').replace("' ",'').replace("] '",']')))
#     dt_temp  = np.array(ast.literal_eval(line_strip.split('timestamp')[1].split('url')[0].replace('],',']').replace("' ",'').replace("] '",']')))
#     #lon_temp = np.array(lon_temp)
#     #lat_temp = np.array(lat_temp) 
#     #dt_temp  = np.array( dt_temp) 
#     lon_temp = lon_temp - lon_temp[0]
#     lat_temp = lat_temp - lat_temp[0] 
#     dt_temp  =  dt_temp -  dt_temp[0] 
#     lon_temp = lon_temp + lon_offset_temp
#     lat_temp = lat_temp + lat_offset_temp
#     dt_temp  =  dt_temp +  dt_offset_temp

# #n_records = 10
# if (f%10 == 0):
#     print ('  processing activity %6.0f of %6.0f with %3.0f n_records and offsets dt %3.0f, lon %5.2f, lat %5.2f ' %(f, n_lines, n_records, dt_offset_temp, lon_offset_temp, lat_offset_temp))
# #print ('  dt min - max is %s - %s ' %(data_temp['timestamp'][0], data_temp['timestamp'][-1] - data_temp['timestamp'][0]))
# #try: 
# #    speed_all.append(data_temp['speed'])
# #except: 
# #    print('f %s mising speed data'%(f))
# #lon_all.append(list(np.array(data_temp['longitude'][0:n_records]) - data_temp['longitude'][0] + lon_offset_temp))
# #lat_all.append(list(np.array(data_temp['latitude'][0:n_records]) - data_temp['latitude'][0] + lat_offset_temp))
# #lat_all.append(list(np.array(data_temp['latitude'][0:n_records)) - data_temp['latitude'][0] + lat_offset_temp))
# #dt_all.append( list(np.array(data_temp['timestamp'][0:n_records]) - data_temp['timestamp'][0] +  dt_offset_temp))
# for n in range(0, n_records, 1):
#     #user_all.append(data_temp['id'])
#     user_all.append(f+1)
#     lon_all.append(lon_temp[n] - lon_temp[0] + lon_offset_temp)
#     lat_all.append(lat_temp[n] - lat_temp[0] + lat_offset_temp)
#     #lat_all.append(list(np.array(data_temp['latitude'][0:n_records)) - data_temp['latitude'][0] + lat_offset_temp))
#     dt_all.append(  dt_temp[n] - dt_temp[0] +   dt_offset_temp)
    
# input_file_open.close()
# time_end = time.time()
# process_dt = (time_end - time_start)/60.0
# print ('read    data took %5.2f minutes ' %(process_dt))


# {'longitude': [24.64977040886879, 24.65014273300767,  24.368406180292368, 24.6496663056314], 
# 'altitude': [41.6, 40.6, 40.6, 38.4], 
# 'latitude': [60.173348765820265, 60.173239801079035, 60.17298021353781, 60.17335429787636], 
# 'sport': 'bike', 
# 'id': 396826535, 
# 'heart_rate': [100, 111, 120, 119], 
# 'gender': 'male', 
# 'timestamp': [1408898746, 1408898754, 1408898765, 1408898778], 
# 'url': 'https://www.endomondo.com/users/10921915/workouts/396826535',
# 'userId': 10921915, 
# 'speed': [6.8652, 16.4736, 19.1988, 20.4804]}


# add random noise to start of tracks
# dt_offset_scaling = 10.0
# lon_offset_scaling = 1.0
# lat_offset_scaling = 1.0
    
# lon_all   = []
# lat_all   = []
# dt_all    = []
# user_all  = []

# n_activities = len(data)
# #n_activities = 10
# f = 0
# for f in range(0, n_activities, 1):
#     dt_offset_temp = int(dt_offset_scaling*random.random())
#     lon_offset_temp = lon_offset_scaling*(random.random()-1.0)
#     lat_offset_temp = lat_offset_scaling*(random.random()-1.0)
#     data_temp = data[f]
#     n_records = len(data_temp['longitude'])
#     #n_records = 10
#     print ('  processing activity %s of %s with %s n_records and offsets dt %3.0f, lon %5.2f, lat %5.2f ' %(f, n_activities, n_records, dt_offset_temp, lon_offset_temp, lat_offset_temp))
#     #print ('  dt min - max is %s - %s ' %(data_temp['timestamp'][0], data_temp['timestamp'][-1] - data_temp['timestamp'][0]))
#     #try: 
#     #    speed_all.append(data_temp['speed'])
#     #except: 
#     #    print('f %s mising speed data'%(f))
#     #lon_all.append(list(np.array(data_temp['longitude'][0:n_records]) - data_temp['longitude'][0] + lon_offset_temp))
#     #lat_all.append(list(np.array(data_temp['latitude'][0:n_records]) - data_temp['latitude'][0] + lat_offset_temp))
#     #lat_all.append(list(np.array(data_temp['latitude'][0:n_records)) - data_temp['latitude'][0] + lat_offset_temp))
#     #dt_all.append( list(np.array(data_temp['timestamp'][0:n_records]) - data_temp['timestamp'][0] +  dt_offset_temp))
#     for n in range(0, n_records, 1):
#         #user_all.append(data_temp['id'])
#         user_all.append(f+1)
#         lon_all.append(data_temp['longitude'][n] - data_temp['longitude'][0] + lon_offset_temp)
#         lat_all.append(data_temp[ 'latitude'][n] - data_temp[ 'latitude'][0] + lat_offset_temp)
#         #lat_all.append(list(np.array(data_temp['latitude'][0:n_records)) - data_temp['latitude'][0] + lat_offset_temp))
#         dt_all.append( data_temp['timestamp'][n] - data_temp['timestamp'][0] +  dt_offset_temp)
