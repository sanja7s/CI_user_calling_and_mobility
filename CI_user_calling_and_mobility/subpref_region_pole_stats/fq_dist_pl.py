'''
Created on Jun 21, 2014

@author: sscepano
'''
from os.path import join
from collections import defaultdict
#######################################################################################      
# this is where we regroup frequency and num dist places per subpref
####################################################################################### 

########################################################
# read in user freq and num distinct places
########################################################
def read_in_user_stats():
                  
    file_name = "/home/sscepano/Project7s/D4D/CI/user_stats/OUTPUTfiles/user_frequency_numDistinctSUBPREFvisited.csv"
    f = open(file_name, "r")
    
    user_stat = defaultdict(int)
    
    for line in f:
        user, fq, dist = line.split(',')
        user = int(user)
        fq = int(fq)
        dist = int(dist)
        
        user_stat[user] = (fq, dist)
    
    return user_stat

########################################################
# read in user freq and num distinct places
########################################################
def read_in_user_home():
                  
    file_name = "/home/sscepano/Project7s/D4D/CI/urban_rural/divide_by_home/OUTPUT_files/users_home.tsv"
    f = open(file_name, "r")
    
    user_home = defaultdict(int)
    
    for line in f:
        user, home = line.split('\t')
        user = int(user)
        home = int(home)
        
        user_home[user] = home
    
    return user_home

########################################################
# divide and save user freq and num distinct places per SUBPREF
########################################################
def save_stats_per_subpref():
    
    location = "/home/sscepano/Project7s/D4D/CI/user_stats/fq_pl/PerSUBPREF"
    
    user_home = read_in_user_home()
    user_stat = read_in_user_stats()
    
    f = defaultdict()
    for i in range (256):
        file_name = "fq_distPl_SUBPREF_" + str(i) + ".tsv"
        save_path = join(location,file_name)
        f[i] = open(save_path, "w")
    
    for usr in user_stat.keys():
        subpref = user_home[usr]
        if subpref <> -1:
            f[subpref].write(str(usr) + '\t' + str(user_stat[usr][0]) + '\t' + str(user_stat[usr][1]) + '\n')
            
   
            
            
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
# divide and save user freq and num distinct places per POLE
########################################################
def save_stats_per_pole():
    
    location = "/home/sscepano/Project7s/D4D/CI/user_stats/fq_pl/PerPOLE"
    
    user_home = read_in_user_home()
    user_stat = read_in_user_stats()
    subpref_region = read_in_subpref_region()
    region_pole = read_in_region_poles_mapping()
    
    f = defaultdict()
    for i in range (12):
        file_name = "fq_distPl_POLE_" + str(i) + ".tsv"
        save_path = join(location,file_name)
        f[i] = open(save_path, "w")
    
    for usr in user_stat.keys():
        subpref = user_home[usr]
        if subpref <> -1:
            if subpref <> 60:
                pole = region_pole[subpref_region[subpref]]
            else: 
                pole = 11
            # these guys exist because we haven't found a home for them, 6 people
            if pole == 0:
                print usr, subpref, subpref_region[subpref]
        
            f[pole].write(str(usr) + '\t' + str(user_stat[usr][0]) + '\t' + str(user_stat[usr][1]) + '\n')
        
        
# save_stats_per_subpref()
save_stats_per_pole()