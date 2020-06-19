# plot_scaling.py
# purpose - plot scaling of spark jobs vs clusters
# usage - IDE


import os 
#import datetime as dt
import numpy as np
import sys 

import matplotlib
#if (run_mode == 'cron'): 
#    matplotlib.use('Agg') 
import matplotlib.pyplot as plt
from matplotlib.dates import drange, DateFormatter
from matplotlib.ticker import MultipleLocator 
import matplotlib.ticker as mticker


dpi_level = 500

dir_work = os.path.join(os.environ['HOME'], 'raceCast')
os.chdir(dir_work)

instances_axis = np.array([   1,    2,    3,    4,    5,    6])
timing =    60.0*np.array([1.62, 1.09, 0.88, 0.77, 0.72, 0.75])
# old
#timing =    60.0*np.array([1.76, 1.26, 1.03, 0.95, 1.09])

fig_num = 201 
fig = plt.figure(num=fig_num,figsize=(10,5)) 
plt.clf() 
plt.plot(instances_axis, timing, 'r', linestyle='-', linewidth=3.0, marker='o', markersize=10, markeredgecolor='k')     

[y_min, y_max, y_int] = [40, 100, 10]

for dum in np.arange(y_min, y_max, y_int):
   plt.plot([0, 7], [dum, dum],  'gray', linestyle='-', linewidth=0.5, marker='o', markersize=0) 
for dum in np.arange(0, 7, 1):
    plt.plot([dum, dum], [0.0, 120.0],  'gray', linestyle='-', linewidth=0.5, marker='o', markersize=0) 
#plt.legend(loc=3,fontsize=10,ncol=1) 
plt.title('spark job run time vs number of t2.medium instances ',\
     fontsize=16, x=0.5, y=1.01,weight = 'bold')
plt.xlabel('number of instances',   fontsize=16,labelpad=0)
plt.ylabel('run time [min]', fontsize=16,labelpad=0)  
#plt.xlim([yy_min-1, yy_max+1])
#minorLocator = MultipleLocator(1)
#plt.gca().yaxis.set_minor_locator(minorLocator)            
plt.xticks(np.arange(0, 7, 1), fontsize=14)
#plt.xlim([0.5, 5.5])
plt.xlim([0.0, 7.0])
plt.yticks(np.arange(y_min, y_max, y_int), fontsize=14)                     
plt.ylim([y_min, y_max])
plt.show() 
filename = 'spark_timing_vs_instances.png'
plot_name = os.path.join(dir_work, 'images', filename)
plt.savefig(plot_name, dpi=dpi_level)



# n_athletes_f = 10.0*np.array([1.0, 2.0, 4.0])
# n_records_f = [1422326.0, 2765267.0, 5558233.0]/1000.0
# throughput_f = [1422326.0/(1000.0*60.0*0.52), 2765267.0/(1000.0*60.0*0.58), 5558233.0/(1000.0*60.0*0.69)]

n_records_per_file = 1422326.0
n_athletes_f = 10.0*np.array([ 1.0,  2.0,  3.0,  4.0,  6.0,  8.0, 10.0, 12.0])
#timing_f =     60.0*np.array([0.43, 0.46, 0.51, 0.54, 0.60, 0.64, 0.73, 0.76])
#timing_f =     60.0*np.array([0.43, 0.46, 0.51, 0.54, 0.60, 0.64, 0.72, 0.76])
timing_f =     60.0*np.array([0.43, 0.46, 0.51, 0.54, 0.60, 0.64, 0.71, 0.76])
# old
#timing_f =          np.array([0.53, 0.58, 0.64, 0.68, 0.79, 0.88, 0.97, 1.06])



# 10 - 0.97 or 1.06
# 12 - 1.03 or 1.06  

throughput_f = n_records_per_file*n_athletes_f/(10.0*1000.0*timing_f) 


#10 - by id old 
#csv_read took   0.39 minutes 
#csv_read took   0.38 minutes 


[x_min, x_max, x_int] = [0, 130.0, 20.0]

fig_num = 203 
fig = plt.figure(num=fig_num,figsize=(10,5)) 
plt.clf() 
plt.plot(n_athletes_f, timing_f, 'r', linestyle='-', linewidth=3.0, marker='o', markersize=10, markeredgecolor='k')     
# plt.plot([x_min, x_max], [60, 60],  'gray', linestyle='-', linewidth=0.5, marker='o', markersize=0) 
[y_min, y_max, y_int] = [25, 50, 5]
for dum in np.arange(y_min, y_max, y_int):
   plt.plot([x_min, x_max], [dum, dum],  'gray', linestyle='-', linewidth=0.5, marker='o', markersize=0) 
for dum in np.arange(x_min, x_max, x_int):
    plt.plot([dum, dum], [y_min, y_max],  'gray', linestyle='-', linewidth=0.5, marker='o', markersize=0) 
#plt.legend(loc=3,fontsize=10,ncol=1) 
plt.title('timing vs number of athletes \n on five t2.medium instances ',\
     fontsize=16, x=0.5, y=1.01,weight = 'bold')
plt.xlabel('number of athletes [x1000]', fontsize=16,labelpad=0)
plt.ylabel('timing [s]', fontsize=16,labelpad=0)  
#plt.xlim([yy_min-1, yy_max+1])
#minorLocator = MultipleLocator(1)
#plt.gca().yaxis.set_minor_locator(minorLocator)            
plt.xticks(np.arange(x_min, x_max, x_int), fontsize=14)
#plt.xlim([0.5, 5.5])
plt.xlim([x_min, x_max])
plt.yticks(np.arange(y_min, y_max, y_int), fontsize=14)                     
plt.ylim([y_min, y_max])
plt.show() 
filename = 'spark_timing_vs_athlete.png'
plot_name = os.path.join(dir_work, 'images', filename)
plt.savefig(plot_name, dpi=dpi_level)




fig_num = 202 
fig = plt.figure(num=fig_num,figsize=(10,5)) 
plt.clf() 
plt.plot(n_athletes_f, throughput_f, 'r', linestyle='-', linewidth=3.0, marker='o', markersize=10, markeredgecolor='k')     
[y_min, y_max, y_int] = [0, 400.0, 50.0]
for dum in np.arange(y_min, y_max, y_int):
   plt.plot([x_min, x_max], [dum, dum],  'gray', linestyle='-', linewidth=0.5, marker='o', markersize=0) 
for dum in np.arange(x_min, x_max, x_int):
    plt.plot([dum, dum], [y_min, y_max],  'gray', linestyle='-', linewidth=0.5, marker='o', markersize=0) 
#plt.legend(loc=3,fontsize=10,ncol=1) 
plt.title('throughput vs number of athletes \n on five t2.medium instances ',\
     fontsize=16, x=0.5, y=1.01,weight = 'bold')
plt.xlabel('number of athletes [x1000]', fontsize=16,labelpad=0)
plt.ylabel('rec/sec [x1000]', fontsize=16,labelpad=0)  
#plt.xlim([yy_min-1, yy_max+1])
#minorLocator = MultipleLocator(1)
#plt.gca().yaxis.set_minor_locator(minorLocator)            
plt.xticks(np.arange(x_min, x_max, x_int), fontsize=14)
#plt.xlim([0.5, 5.5])
plt.xlim([x_min, x_max])
plt.yticks(np.arange(y_min, y_max, y_int), fontsize=14)                     
plt.ylim([y_min, y_max])
plt.show() 
filename = 'spark_throughput_vs_athlete.png'
plot_name = os.path.join(dir_work, 'images', filename)
plt.savefig(plot_name, dpi=dpi_level)





