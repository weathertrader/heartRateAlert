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

dir_work = os.path.join(os.environ['HOME'], 'raceCast')
os.chdir(dir_work)

instances_axis = [1,2,3,4,5]
timing = [1.76, 1.26, 1.03, 0.95, 1.09]

fig_num = 201 
fig = plt.figure(num=fig_num,figsize=(10,5)) 
plt.clf() 
plt.plot(instances_axis, timing, 'r', linestyle='-', linewidth=3.0, marker='o', markersize=10, markeredgecolor='k')     
for dum in np.arange(0.0, 2.0, 0.2):
   plt.plot([0, 6], [dum, dum],  'gray', linestyle='-', linewidth=0.5, marker='o', markersize=0) 
for dum in np.arange(0, 6, 1):
    plt.plot([dum, dum], [0.0, 2.0],  'gray', linestyle='-', linewidth=0.5, marker='o', markersize=0) 
#plt.legend(loc=3,fontsize=10,ncol=1) 
plt.title('spark job run time vs number of t2.medium instances ',\
     fontsize=16, x=0.5, y=1.01,weight = 'bold')
plt.xlabel('number of instances',   fontsize=16,labelpad=0)
plt.ylabel('run time [min]', fontsize=16,labelpad=0)  
#plt.xlim([yy_min-1, yy_max+1])
#minorLocator = MultipleLocator(1)
#plt.gca().yaxis.set_minor_locator(minorLocator)            
plt.xticks(np.arange(0, 6, 1), fontsize=14)
#plt.xlim([0.5, 5.5])
plt.xlim([0.0, 6.0])
plt.yticks(np.arange(0.0, 2.0, 0.2), fontsize=14)                     
plt.ylim([0.0, 2.0])
plt.show() 
filename = 'spark_timing_vs_instances.png'
plot_name = os.path.join(dir_work, 'images', filename)
plt.savefig(plot_name)



