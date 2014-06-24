'''
Created on Jun 24, 2014

@author: sscepano
'''
########################################################
### recalculate frequency and num visited places per admin unit
### and sum the subprefs into regions OR development poles
########################################################
from collections import defaultdict

########################################################
# just save this output for development poles, separate Abidjan
########################################################
def save_dev_poles_user_stats():
    
    pole_stats = calculate_dev_pole_stat()
    
    file_name = "/home/sscepano/Project7s/D4D/CI/call_timings/pole/pole_peaks_ratio.tsv"
    f = open(file_name, "w")
    
    for pole in pole_stats.keys():
        f.write(str(pole) + '\t' + str(pole_stats[pole]) + '\n')
        
 
########################################################
# YOU NEED TO RECALCULATE THIS ONE FOR -1 
########################################################          
########################################################
# sum user stats into pole (subpref --> region --> dev pole)
########################################################        
def calculate_dev_pole_stat():
    
    # this dict has tuple elements (fq, dist)
    subpref_ratio = read_in_subpref_ratio()
    subpref_region = read_in_subpref_region()
    region_pole = read_in_region_poles_mapping()
    
    pole_stats = defaultdict(int)
    pole_subprefs = defaultdict(int)
    
    for subpref in subpref_ratio.keys():
        if subpref == -1 or subpref == 0:
            continue
        if subpref <> 60:
            pole = region_pole[subpref_region[subpref]]
        else: 
            pole = 11
        pole_stats[pole] += subpref_ratio[subpref]
        pole_subprefs[pole] += 1
    
    pole_stats_fin = defaultdict(int)
           
    for pole in pole_stats.keys():
        pole_stats_fin[pole] = pole_stats[pole]/float(pole_subprefs[pole])
        
    return pole_stats_fin


def read_in_pole_users():
    
    pole_users = defaultdict(int)
    
    file_name = "/home/sscepano/Project7s/D4D/CI/users_population_density/pole_num_users.tsv"
    f = open(file_name, "r")
    
    for line in f:
        pole, users = line.split('\t')
        pole = int(pole)
        users = int(users)
        
        pole_users[pole] = users
        
    return pole_users


def read_in_region_poles_mapping():
    
    file_name = "/home/sscepano/Project7s/D4D/CI/admin_units/regions_and_poles/regions_poles_mapping.csv"
    f = open(file_name, "r")
    
    region_pole = defaultdict(int)
    
    for line in f:
        region, pole = line.split(',')
        region = int(region)
        pole = int(pole)
        
        region_pole[region] = pole
        
    print region_pole.values()
        
    return region_pole


########################################################
# mask for subprefs into regions
########################################################
def read_in_subpref_region():
                  
    file_name = "/home/sscepano/DATA SET7S/D4D/Regions/Region_subprefs_mapping.csv"
    f = open(file_name, "r")
    
    subpref_region = defaultdict(int)
    
    for line in f:
        region, subpref = line.split(',')
        region = int(region)
        subpref = int(subpref)
        
        subpref_region[subpref] = region
    
    return subpref_region


########################################################
# read in user freq and num distinct places
########################################################
def read_in_subpref_ratio():
                  
    file_name = "/home/sscepano/Project7s/D4D/CI/call_timings/subpref_ratio_calling_peak.tsv"
    f = open(file_name, "r")
    
    subpref_ratio = defaultdict(int)
    
    for line in f:
        subpref, ratio = line.split('\t')
        subpref = int(subpref)
        ratio = float(ratio)
        
        subpref_ratio[subpref] = ratio
    
    return subpref_ratio



# calculate_dev_pole_stat()
save_dev_poles_user_stats()