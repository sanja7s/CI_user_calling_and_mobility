'''
Created on Aug 12, 2014

@author: sscepano
'''
from os.path import isfile, join
from collections import defaultdict
from multiprocessing import Pool
from itertools import repeat
from datetime import date,timedelta

# function for multithread support
def f((data, i)):
    data = read_in_call_timing(i, data)
    return data

# function to read A ... Z files in parallel
def read_in_all_multiprocessing():
    
    data = defaultdict(int)
    
    for subpref in range(256):
        data[subpref] = defaultdict(int)
        for i in range(24):
            data[subpref][i] = defaultdict(int)
            for j in range(60):
                data[subpref][i][j] = defaultdict(int)
       
    print "Read data USING POOL started"
    p = Pool(processes=10)         
    data2 = p.map(f, zip(repeat(data), list(map(chr, range(ord('A'), ord('J')+1)))))
    
    return data2


def read_in_call_timing(c, data):
    
    i = 0
    #data = defaultdict(int)
    
    D4D_path_SET3 = "/home/sscepano/DATA SET7S/D4D/SET3TSV"
    file_name = "SUBPREF_POS_SAMPLE_" + c + ".TSV"
    f_path = join(D4D_path_SET3,file_name)
    if isfile(f_path) and file_name != '.DS_Store':
            file7s = open(f_path, 'r')
            for line in file7s:
                i = i + 1
                usr, call_time, subpref = line.split('\t')
                subpref = subpref[:-1]
                subpref = int(subpref)
                if subpref <> -1:
                    #print subpref
                    call_hour = int(call_time[11:13])
                    call_min = int(call_time[14:17][:-1])
                    call_date = date(int(call_time[:4]), int(call_time[5:7]), int(call_time[8:10]))
                    if call_date.weekday() >= 5:
                        data[subpref][call_hour][call_min]['weekend'] += 1
                    else:
                        data[subpref][call_hour][call_min]['weekday'] += 1
  
    print i            
    return data