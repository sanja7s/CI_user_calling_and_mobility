'''
Created on Jun 19, 2014

@author: sscepano
'''
from os.path import isfile, join
from collections import defaultdict
from multiprocessing import Pool
from itertools import repeat
#######################################################################################      
# this one is for calling other functions needed with the data
####################################################################################### 

# function for multithread support
def f((data, i)):
    data = read_in_radius_gyration(i, data)
    return data

# function to read A ... Z files in parallel
def read_in_all_multiprocessing():
    
    data = defaultdict(int)
    
    for usr in range(500001):
        data[usr] = defaultdict(int)
        
    print "Read data USING POOL started"
    p = Pool(processes=10)         
    data2 = p.map(f, zip(repeat(data), list(map(chr, range(ord('A'), ord('J')+1)))))
    
    return data2

# this is to read in radius of gyration
# we need user trajectory in order to follow the visited places
# as radius gyration calculation at any moment needs whole list
# of so far visited places
def read_in_radius_gyration(c, usr_traj):
   
    print "Read data started for " + c  
    # lines read in
    i = 0
    
    D4D_path_SET3 = "/home/sscepano/DATA SET7S/D4D/SET3TSV"
    file_name = "SUBPREF_POS_SAMPLE_" + c + ".TSV"
    #file_name = '100Klines.txt'
    f_path = join(D4D_path_SET3,file_name)
    if isfile(f_path) and file_name != '.DS_Store':
            file7s = open(f_path, 'r')
            for line in file7s:
                i = i + 1
                usr, call_time, subpref = line.split('\t')
                usr = int(usr)
                subpref = int(subpref)
                # for each user we hold a dictionary with all the visited subprefs and the number of visits to each
                # this is done by increasing the number in the dict each time user visits the subpref
                usr_traj[usr][subpref] += 1 
                if i in [10000, 100000, 1000000, 10000000, 100000000]:
                    print i, len(usr_traj[usr])
    
    print i     
    print "Read data finished for " + c         
    return usr_traj