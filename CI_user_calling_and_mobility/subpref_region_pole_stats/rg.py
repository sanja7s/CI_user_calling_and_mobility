'''
Created on Jun 24, 2014

@author: sscepano
'''
'''
Created on Jun 21, 2014

@author: sscepano
'''
from os.path import join
from collections import defaultdict
#######################################################################################      
# this is where we regroup RG per subpref
####################################################################################### 

########################################################
# 1 read in user rg
########################################################
def read_in_user_stats():
                  
    file_name = "/home/sscepano/Project7s/D4D/CI/user_stats/OUTPUTfiles/usr_radius_gyr.tsv"
    f = open(file_name, "r")
    
    user_stat = defaultdict(int)
    
    for line in f:
        user, r = line.split('\t')
        user = int(user)
        r = float(r)
        
        user_stat[user] = r
    
    return user_stat


########################################################
# read in user home
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
# divide and save user rg per SUBPREF
########################################################
def save_stats_per_subpref():
    
    location = "/home/sscepano/Project7s/D4D/CI/user_stats/Rg/perSUBPREF"
    
    user_home = read_in_user_home()
    user_stat = read_in_user_stats()
    
    f = defaultdict()
    for i in range (256):
        file_name = "rg_" + str(i) + ".tsv"
        save_path = join(location,file_name)
        f[i] = open(save_path, "w")
    
    for usr in user_stat.keys():
        subpref = user_home[usr]
        if subpref <> -1:
            f[subpref].write(str(usr) + '\t' + str(user_stat[usr]) + '\n')
            
            
            
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
# divide and save user rg per POLE
########################################################
def save_stats_per_pole():
    
    location = "/home/sscepano/Project7s/D4D/CI/user_stats/Rg/perPOLE"
    
    user_home = read_in_user_home()
    user_stat = read_in_user_stats()
    subpref_region = read_in_subpref_region()
    region_pole = read_in_region_poles_mapping()
    
    f = defaultdict()
    for i in range (12):
        file_name = "rg_POLE_" + str(i) + ".tsv"
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
        
            f[pole].write(str(usr) + '\t' + str(user_stat[usr]) +  '\n')
        
        
save_stats_per_subpref()

# save_stats_per_pole()