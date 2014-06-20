'''
Created on Jun 20, 2014

@author: sscepano
'''
from os.path import isfile, join
from collections import defaultdict
import math
import numpy as n
from multiprocessing import Pool
from itertools import repeat
#######################################################################################      
# this one is for calling other functions needed with the data
####################################################################################### 

# function for multithread support
def f((data, i)):
    data = read_in_file_avg_daily_traj(i, data)
    return data

# function to read A ... Z files in parallel
def read_in_all_multiprocessing():
    
    usr_traj = defaultdict(int)
    usr_day = defaultdict(int)
    usr_traj_today = defaultdict(int)
    for i in range(500001):
        usr_day[i] = defaultdict(int)
        usr_traj_today[i] = defaultdict(int)
      
    data = (usr_traj, usr_day, usr_traj_today)
 
    print "Read data USING POOL started"
    p = Pool(processes=10)         
    data2 = p.map(f, zip(repeat(data), list(map(chr, range(ord('A'), ord('J')+1)))))
    
    return data2



# we want avg traveled dist on daily basis
def read_in_file_avg_daily_traj(c, data):
    
    usr_traj, usr_day, usr_traj_today = data[0], data[1], data[2]
    
    subpref_dist = find_subpref_distance()
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
                #call_time = datetime.strptime(call_time, '%Y-%m-%d %H:%M:%S')
                call_day = call_time[0:10]
                #print call_day
                
                if usr_day[usr][0] == call_day:
                    # for each user we hold a dictionary with all the visited subprefs and the number of visits to each
                    # this is done by increasing the number in the dict each time user visits the subpref
                    old_loc = usr_traj_today[usr][1]  
                    usr_traj_today[usr][0] += subpref_dist[old_loc,subpref]
                    usr_traj_today[usr][1] = subpref
                    #print usr_traj_today[usr][1], usr_traj_today[usr][0]
                else:
                    #print usr_traj_today[usr][0]
                    usr_day[usr][1] += 1
                    usr_day[usr][0] = call_day
                    usr_traj[usr] += usr_traj_today[usr][0]
                    usr_traj_today[usr][1] = subpref
                    usr_traj_today[usr][0] = 0
                    #print
    
    print i            
    return (usr_traj, usr_day, usr_traj_today)



def find_subpref_distance():
    
    ant_pos_data = read_in_subpref_pos_file()   
    ant_dist_data = n.zeros((1239,1239), dtype=n.float)
    
    R = 6371
    file_name = "/home/sscepano/Project7s/D4D/CI/admin_units/subprefs/subpref_distances_file.tsv"
    f = open(file_name,"w")
    
    for subpref1 in range(256):
        for subpref2 in range(256):
                lon1 = ant_pos_data[subpref1][0]
                lat1 = ant_pos_data[subpref1][1]
                lon2 = ant_pos_data[subpref2][0]
                lat2 = ant_pos_data[subpref2][1]
                
                dLat = math.radians(lat2-lat1)
                dLon = math.radians(lon2-lon1)
                lat1 = math.radians(lat1)
                lat2 = math.radians(lat2)
                a = math.sin(dLat/2) * math.sin(dLat/2) + math.sin(dLon/2) * math.sin(dLon/2) * math.cos(lat1) * math.cos(lat2)
                c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
                dist = R * c
                
                ant_dist_data[subpref1][subpref2] = dist
                f.write(str(subpref1) + '\t' + str(subpref2) + '\t' + str(dist) + '\n')
                               
    return ant_dist_data  


# subpref positions
def read_in_subpref_pos_file():
    
    subpref_pos_data = n.zeros((256,2))
    
    D4D_path_SET3 = "/home/sscepano/DATA SET7S/D4D"
    file_name = "SUBPREF_POS_LONLAT.TSV"
    f_path = join(D4D_path_SET3,file_name)
    if isfile(f_path) and file_name != '.DS_Store':
            file7s = open(f_path, 'r')
            for line in file7s:
                subpref, lon, lat = line.split('\t')
                subpref = int(subpref)
                lon = float(lon)
                lat = float(lat)
                subpref_pos_data[subpref][0] = lon
                subpref_pos_data[subpref][1] = lat
                
    return subpref_pos_data