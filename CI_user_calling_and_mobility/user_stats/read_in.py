'''
Created on Jun 16, 2014

@author: sscepano
'''
from os.path import isfile, join
from collections import defaultdict
from multiprocessing import Pool
from itertools import repeat

# function for multithread support
def f((data, i)):
    data = read_in_fq_distinct_places(i, data)
    return data

# function to read A ... Z files in parallel
def read_in_all_multiprocessing():
    
    data = defaultdict(int)
    
    print "Read data USING POOL started"
    p = Pool(processes=10)         
    data2 = p.map(f, zip(repeat(data), list(map(chr, range(ord('A'), ord('J')+1)))))
    
    return data2

def read_in_fq_distinct_places(c, data):
    
    print "Read data started for " + c  
    # lines read in
    i = 0
    
    D4D_path_SET3 = "/home/sscepano/DATA SET7S/D4D/SET3TSV"
    file_name = "SUBPREF_POS_SAMPLE_" + c + ".TSV"
    f_path = join(D4D_path_SET3,file_name)
    if isfile(f_path) and file_name != '.DS_Store':
            file7s = open(f_path, 'r')
            for line in file7s:
                i = i + 1
                user, call_time, subpref = line.split('\t')
                user = int(user)
                subpref = int(subpref[:-1])
                data[user] = data.get(user, defaultdict(int))
                data[user]['subpref'] = data[user].get('subpref', defaultdict(int))
                # just from time to time testing printing to know we are reading in still
                if i in [10000, 100000, 1000000, 10000000, 100000000]:
                    print i, len(data[user]), len(data[user]['subpref'])
                
                # for the number of calls    
                data[user]['fq'] += 1
                # for the number of distinct subprefs visited
                data[user]['subpref'][subpref] = 1

    
    print i     
    print "Read data finished for " + c       
    return data