# produce_stream.py 
# streams gps data to pulsar cluster 
# usage: 
# python src/produce_stream.py 2 1 0.0
# python src/produce_stream.py 4 2 0.01
# command line arguments are n_cores, core_delay, line_delay

import os
import sys
import time
import csv
#import ast
from datetime import datetime as dt
import subprocess
import multiprocessing
from multiprocessing import Process
#import pandas as pd
#import numpy as np
#import csv
#import psutil
#from multiprocessing import Pool

# dir_work = '/home/craigmatthewsmith/raceCast'
# os.chdir(dir_work)
# dir_work = os.getcwd()
#print('working directory is %s ' %(os.getcwd()))
# input_file = 'data/gps_tracks_processed_0.csv'
# os.path.isfile(input_file)

# os.cpu_count()
# psutil.cpu_count()
# psutil.cpu_count(logical=False)
# psutil.cpu_count(logical=True)

# debugging 
# input_file = 'data/processed_data_0.csv'
#dir_work = '/home/craigmatthewsmith/raceCast'
#os.chdir(dir_work)

def stream_data(input_file, line_delay):
        
    time_start = time.time()
    print ('    read data ')
    
    #read_method = 'all'
    read_method = 'line'
    
    if (read_method == 'all'):
        input_file_open = open(input_file,'r')
        print('    input file open')
        file_lines = input_file_open.readlines()
        n_lines = len(file_lines)
        print('    found %s lines' %(n_lines))    
        n = 6 
        for n in range(1, n_lines, 1): 
            [entry, dt_temp, id_temp, lon_temp, lat_temp] = map(float, file_lines[n].rstrip().split(','))
            print(' streaming n %8.0f of %8.0f, dt %6.0f, id %6.0f' %(n, n_lines, dt_temp, id_temp))
            time.sleep(line_delay)    
        input_file_open.close()
    
    elif (read_method == 'line'):
        n = 0
        with open(input_file, 'r', encoding='utf-8') as input_file_open: 
            next(input_file_open)
            for row in csv.reader(input_file_open):
                while (n < 20):
                    #[entry, dt_temp, id_temp, lon_temp, lat_temp] = map(float, row.rstrip().split(','))
                    [entry, dt_temp, id_temp, lon_temp, lat_temp] = map(float, row)
                    #print(' streaming n %8.0f of %8.0f, dt %6.0f, id %6.0f' %(n, n_lines, dt_temp, id_temp))
                    print('    streaming n %8.0f dt %6.0f, id %6.0f' %(n, dt_temp, id_temp))
                    time.sleep(line_delay)   
                    n += 1

    time_end = time.time()
    process_dt = (time_end - time_start)/60.0
    print ('    stream data took %5.2f minutes ' %(process_dt))
   
if __name__ == '__main__':
    # n_cores = 2
    # ramp_delay = 5
    # line_delay = 0.0
    # takes 18 min w/ delay amount = 0
    #line_delay = 0.000001
    # line_delay = 0.0

    #n_cores    = sys.argv[1]
    #core_delay = sys.argv[2]
    #line_delay = sys.argv[3]
    n_cores    =   int(sys.argv[1])
    core_delay = float(sys.argv[2])
    line_delay = float(sys.argv[3])
    # only 8 files available to stream 
    n_max_cores = multiprocessing.cpu_count()
    n_cores = min(n_cores, n_max_cores)
    print('using %s of %s cores with %6.2f file_delay and %8.7f line_delay' %(n_cores, n_max_cores, core_delay, line_delay))
    for cpu in range(0, n_cores, 1):
        input_file = 'data/gps_tracks_processed_'+str(cpu)+'.csv'
        print('  submitting core %s ' %(input_file))
        #stream_data(input_file, line_delay)
        temp_command = 'stream_data('+input_file+', '+str(line_delay)+')'
        print('  submit command in %s ' %(temp_command))
        #subprocess.Popen(temp_command, shell=True)
        p = Process(target=stream_data, args=(input_file, line_delay))
        p.start()
        #p.join() # this blocks until the process terminates
        #result = queue.get()
        # print result
        print('  job submitted ')
        print('  sleep begin ')
        time.sleep(core_delay)
        print('  sleep end ')

