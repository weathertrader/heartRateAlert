# data_preprocess.py 
# reads in raw gps data and write a csv ordered by timestamp 
# usage: 
# python preprocess/data_preprocess.py data/endomondoHR_proper.json processed_data.csv
# python preprocess/data_preprocess.py data/gps_tracks_0.txt gps_tracks_processed_0.csv

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

#manual_debug = False
manual_debug = True
if (manual_debug):
    base_dir = '/home/craigmatthewsmith'
    work_dir = os.path.join(base_dir, 'raceCast')
    os.chdir(work_dir)
else:
    work_dir = os.getcwd()

#def preprocess_inputs(input_file, output_file):
def preprocess_inputs():
    
    print('file read begin ')

    #file_name_data = os.path.join(dir_data, 'data_subset_proper.json')
    #os.path.isfile(file_name_data)
    #data = []
    #with open(input_file) as file_open:
    #    for line in file_open:
    #        data.append(eval(l))
            
    # add random noise to start of tracks
    #dt_offset_scaling  = 10.0
    #lon_offset_scaling = 1.0
    #lat_offset_scaling = 1.0

    n_records = 500
    #n_activities = 168000
    # 83892000
    # chokes 
    n_activities = 20000
    
    #n_subset = int(168000/n_activities)+1

    #subset = 5
    #for subset in range(4, n_subset, 1):
    #start_count = subset*n_activities
    #end_count = start_count + n_activities
    #print ('  subset %6.0f of %6.0f, start_count %6.0f, end_count %6.0f ' %(subset, n_subset, start_count, end_count))
 
 
    #data_all   = np.full([n_activities*n_records,4], np.nan, dtype=float)


    # dt_max is 17985.0 or 5.0 hours, should dt_all = dt_all/10.0, would need to cast to float

    max_records_per_batch = 40000000 # 24,000,000
    #                       10,000,000

    n_batch = 20
    dt_max_expected = 20000.0
    dt_int = dt_max_expected/n_batch
    n = 1
    #for n in range(0, n_batch, 1):
    for n in range(2, 4, 1):
        count_all = 0
        [dt_min_n, dt_max_n] = [n*dt_int, (n+1)*dt_int]
        print('  processing n %s of %s, dt %s - %s ' %(n, n_batch, dt_min_n, dt_max_n))
        #output_file = 'data/gps_tracks_stream_minute_'+str(n)+'.csv'    
        output_file = 's3a://gps-data-processed/gps_tracks_stream_minute_'+str(n)+'.csv'    

        lon_all = np.full([max_records_per_batch], np.nan, dtype=float)
        lat_all = np.full([max_records_per_batch], np.nan, dtype=float)
        dt_all  = np.full([max_records_per_batch], 0, dtype=int)
        id_all  = np.full([max_records_per_batch], 0, dtype=int)
        hr_all  = np.full([max_records_per_batch], 0, dtype=int)
        
        n_files = 9        
        #for f in range(0, n_files, 1):
        for f in range(0, 2, 1):
            input_file  = 'data/gps_tracks_'+str(f)+'.txt'
            #input_file  = 's3a://gps-data-processed/gps_tracks_'+str(f)+'.txt'
            id_start = n_activities*f
            print('    processing f %s of %s, id_start %s, %s ' %(f, n_files, id_start, input_file))        
            time_start = time.time()
            print('      read data begin ')
        
            lon_file = np.full([n_activities*n_records], np.nan, dtype=float)
            lat_file = np.full([n_activities*n_records], np.nan, dtype=float)
            #dt_file  = np.full([n_activities*n_records], 0, dtype=int)
            dt_file  = np.full([n_activities*n_records], dt_min_n-1, dtype=int)
            #id_file  = np.full([n_activities*n_records], 0, dtype=int)
            id_file  = np.full([n_activities*n_records], id_start, dtype=int)
            hr_file  = np.full([n_activities*n_records], 0, dtype=int)

            line_count = 0
            count_file = 0
                       
            dt_min = 100000000000
            dt_max = 0
            
            with open(input_file) as file_open:
                for line in file_open:
                    #if (line_count%100 == 0):
                    #    print ('      line_count %6.0f start_count %6.0f end_count %6.0f ' %(line_count, start_count, end_count))
                    #    #print ('     line_count %6.0f with %3.0f n_records and offsets dt %3.0f, lon %5.2f, lat %5.2f ' %(line_count, n_records, dt_offset_temp, lon_offset_temp, lat_offset_temp))
                    #if (line_count < start_count):
                    #    next(file_open)
                    #if (line_count < n_activities):
                    #elif (line_count >= start_count and line_count < end_count):
                    # can skip lines using 
                    #next(f)
                    #dt_offset_temp = int(dt_offset_scaling*random.random())
                    #dt_offset_temp = float(dt_offset_scaling*random.random())
                    #lon_offset_temp = lon_offset_scaling*(random.random()-1.0)
                    #lat_offset_temp = lat_offset_scaling*(random.random()-1.0)
                    #file_line_temp = "{'longitude': [24.64977040886879, 24.65014273300767,  24.368406180292368, 24.6496663056314], 'altitude': [41.6, 40.6, 40.6, 38.4], 'latitude': [60.173348765820265, 60.173239801079035, 60.17298021353781, 60.17335429787636], 'sport': 'bike', 'id': 396826535, 'heart_rate': [100, 111, 120, 119], 'gender': 'male', 'timestamp': [1408898746, 1408898754, 1408898765, 1408898778], 'url': 'https://www.endomondo.com/users/10921915/workouts/396826535','userId': 10921915, 'speed': [6.8652, 16.4736, 19.1988, 20.4804]}"        
                    #line_strip = file_line_temp.replace(':','').replace('{','').replace('}','')
                    #line_strip = file_lines[f].replace(':','').replace('{','').replace('}','')        
                    line_strip = line.replace(':','').replace('{','').replace('}','')        
                    lon_temp = np.array(ast.literal_eval(line_strip.split('longitude')[1].split('altitude')[0].replace('],',']').replace("' ",'').replace("] '",']')))
                    lat_temp = np.array(ast.literal_eval(line_strip.split('latitude')[1].split('sport')[0].replace('],',']').replace("' ",'').replace("] '",']')))
                    dt_temp  = np.array(ast.literal_eval(line_strip.split('timestamp')[1].split('url')[0].replace('],',']').replace("' ",'').replace("] '",']')))
                    hr_temp  = np.array(ast.literal_eval(line_strip.split('heart_rate')[1].split('gender')[0].replace('],',']').replace("' ",'').replace("] '",']')))
        
                    #lon_temp = np.array(lon_temp)
                    #lat_temp = np.array(lat_temp) 
                    #dt_temp  = np.array( dt_temp) 
                    lon_temp = lon_temp - lon_temp[0]
                    lat_temp = lat_temp - lat_temp[0] 
                    dt_temp  =  dt_temp -  dt_temp[0] 
                    #lon_temp = lon_temp + lon_offset_temp
                    #lat_temp = lat_temp + lat_offset_temp
                    #dt_temp  =  dt_temp +  dt_offset_temp
        
                    #dt_max_temp = np.nanmax(dt_temp)
                    #if (dt_min_temp < dt_min):
                    #    print('dt min max first last is %5.2f, %5.2f, %5.2f, %5.2f' %(dt_min_temp, dt_max_temp, dt_temp[0], dt_temp[-1]))
                    #    dt_min = dt_min_temp
                    #if (dt_max_temp < dt_max):
                    #    print('dt min max first last is %5.2f, %5.2f, %5.2f, %5.2f' %(dt_min_temp, dt_max_temp, dt_temp[0], dt_temp[-1]))
                    #    dt_max = dt_max_temp
                    dt_min_temp = np.nanmin(dt_temp)
                    dt_max_temp = np.nanmax(dt_temp)
                    #if (dt_min_temp < 0) or (dt_max_temp > 28800.0):
                    #    print('    dt min max first last is %8.0f, %8.0f, %8.0f, %8.0f' %(dt_min_temp, dt_max_temp, dt_temp[0], dt_temp[-1]))
                    #else: 
                    if ((dt_min_temp >= 0) and (dt_max_temp < 28800.0)):
                        #n_records = len(lon_temp)
                        #n_records = 10
                        print_progress = False
                        if (print_progress):
                            if (line_count%1000 == 0):
                                #print ('    count %6.0f line_count %6.0f with %3.0f n_records and offsets dt %3.0f, lon %5.2f, lat %5.2f ' %(count, line_count, n_records, dt_offset_temp, lon_offset_temp, lat_offset_temp))
                                print ('      count %6.0f dt min max is %6.0f %6.0f ' %(line_count, dt_temp[0], dt_temp[-1]))
            
                        id_file [(line_count*n_records):(line_count*n_records+n_records)] = id_start + line_count+1
                        dt_file [(line_count*n_records):(line_count*n_records+n_records)] =  dt_temp
                        lon_file[(line_count*n_records):(line_count*n_records+n_records)] = lon_temp
                        lat_file[(line_count*n_records):(line_count*n_records+n_records)] = lat_temp
                        hr_file [(line_count*n_records):(line_count*n_records+n_records)] = hr_temp
                        line_count += 1

            time_end = time.time()
            process_dt = (time_end - time_start)/60.0
            # takes 10 min
            print('      read data took %5.2f minutes ' %(process_dt))               
            print('      file read end ')

            print('      mask arrays before')

            # print min and max values 
            print ('      dt   min - max is %5.0f - %5.0f' %(np.nanmin( dt_file), np.nanmax( dt_file)))
            print ('      id   min - max is %5.0f - %5.0f' %(np.nanmin( id_file), np.nanmax( id_file)))
            #print ('    lon  min - max is %5.2f - %5.2f' %(np.nanmin(lon_file), np.nanmax(lon_file)))
            #print ('    lat  min - max is %5.2f - %5.2f' %(np.nanmin(lat_file), np.nanmax(lat_file)))
            #print ('    hr   min - max is %5.2f - %5.2f' %(np.nanmin( hr_file), np.nanmax( hr_file)))

            print('    mask arrays after')
            mask = ((dt_file >= dt_min_n) & (dt_file < dt_max_n))

            id_file  =  id_file[mask]
            dt_file  =  dt_file[mask]
            lon_file = lon_file[mask]
            lat_file = lat_file[mask]
            hr_file  =  hr_file[mask]
            del mask
            # print min and max values 
            print ('      dt   min - max is %5.0f - %5.0f' %(np.nanmin( dt_file), np.nanmax( dt_file)))
            print ('      id   min - max is %5.0f - %5.0f' %(np.nanmin( id_file), np.nanmax( id_file)))
            #print ('    lon  min - max is %5.2f - %5.2f' %(np.nanmin(lon_file), np.nanmax(lon_file)))
            #print ('    lat  min - max is %5.2f - %5.2f' %(np.nanmin(lat_file), np.nanmax(lat_file)))
            #print ('    hr   min - max is %5.2f - %5.2f' %(np.nanmin( hr_file), np.nanmax( hr_file)))
            count_file = len(id_file)
            
            print('      count_all %s, count_file %s, line_count %s' %(count_all, count_file, line_count))

            id_all [count_all:count_all+count_file] =  id_file
            lon_all[count_all:count_all+count_file] = lon_file
            lat_all[count_all:count_all+count_file] = lat_file
            dt_all [count_all:count_all+count_file] =  dt_file
            hr_all [count_all:count_all+count_file] =  hr_file

            count_all = count_all + count_file

        print('  done reading all files ')
        print('  truncate arrays ')
        print('  shape is %s ' %(len(lon_all)))
              
        lon_all = lon_all[0:count_all]
        lat_all = lat_all[0:count_all]
        id_all  =  id_all[0:count_all]
        dt_all  =  dt_all[0:count_all]
        hr_all  =  hr_all[0:count_all]

        print('  final shape is %s ' %(len(lon_all)))

        # print min and max values 
        print ('  final min max values ')
        print ('  dt   min - max is %5.0f - %5.0f' %(np.nanmin( dt_all), np.nanmax( dt_all)))
        print ('  id   min - max is %5.0f - %5.0f' %(np.nanmin( id_all), np.nanmax( id_all)))
        print ('  lon  min - max is %5.2f - %5.2f' %(np.nanmin(lon_all), np.nanmax(lon_all)))
        print ('  lat  min - max is %5.2f - %5.2f' %(np.nanmin(lat_all), np.nanmax(lat_all)))
        print ('  hr   min - max is %5.2f - %5.2f' %(np.nanmin( hr_all), np.nanmax( hr_all)))
 
        print('  sort by time start ')
        index_sort = np.argsort(dt_all)    
        data_df = pd.DataFrame(data={'dt' : dt_all [index_sort],
                                     'id' : id_all [index_sort],
                                     'lon': lon_all[index_sort],
                                     'lat': lat_all[index_sort],
                                     'hr' : hr_all [index_sort]})
        
        
        #data_df.sort_values(['id', 'dt'], ascending=[True, True], inplace=True)  
        
        #data_all = np.array([dt_all[index_sort], id_all[index_sort], lon_all[index_sort], hr_all[index_sort], lat_all[index_sort]]).T
        print('  sort by time end ')
        print('  output_file is %s ' %(output_file))
        print('  write file start ')
        data_df.to_csv(output_file) 
        print('  write file end ')

        del id_all, lon_all, lat_all, hr_all
        
        #data_array = np.stack([dt_all, id_all, lon_all, lat_all], axis=0) # .T
        # del dt_all, id_all, lon_all, lat_all
    
        #column_str = ['dt', 'id', 'lon', 'lat', 'hr']
        #data_df = pd.DataFrame (data_array, columns=column_str)
        #data_df = pd.DataFrame (data_all.T, columns=column_str)
        #data_df = pd.DataFrame (data_all, columns=column_str)
        #del data_all
        #data_df.sort_values(by=['dt', 'user'])
        #data_df = data_df.sort_values(by=['dt', 'user'])
        #print('    sort df start ')
        #data_df = data_df.sort_values(by=['dt'])
        #print('    sort df end ')
        #processed_data_file_name = os.path.join(dir_work,'processed_data.csv')
        #processed_data_file_name = os.path.join(dir_work,'processed_data_subset_'+str(subset)+'.csv')
        #print('    processed_data_file_name is %s ' %(processed_data_file_name))
        #data_df.to_csv(processed_data_file_name) 
    
        #data_df.head(40)

        # note csmith - here should mask out hr < 30        
        # zero out dt, lon, and lat globally
        #lon_file = lon_file - np.nanmin(lon_file)
        #lat_file = lat_file - np.nanmin(lat_file)
        #dt_file  =  dt_file - np.nanmin( dt_file)

if __name__ == '__main__':
    #input_file  = sys.argv[1]
    #output_file = sys.argv[2]
    #print('using input  file %s ' %(input_file))
    #print('using output file %s ' %(output_file))
    preprocess_inputs()


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
#     #lat_temp = np.array(lat_temp) #     #dt_temp  = np.array( dt_temp) 
#     lon_temp = lon_temp - lon_temp[0]
#     lat_temp = lat_temp - lat_temp[0] 
#     dt_temp  =  dt_temp -  dt_temp[0] 
#     lon_temp = lon_temp + lon_offset_temp
#     lat_temp = lat_temp + lat_offset_temp
#     dt_temp  =  dt_temp +  dt_offset_temp


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

