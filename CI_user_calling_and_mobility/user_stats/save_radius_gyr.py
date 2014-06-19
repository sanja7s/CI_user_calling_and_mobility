'''
Created on Jun 19, 2014

@author: sscepano
'''
from collections import defaultdict
from os.path import isfile, join
import math
import numpy as n
#######################################################################################      
# this one is for calculating and saving radius of gyration
#######################################################################################  


def save_radius_gyr(usr_traj):
    
    rg = calculate_radius_gyration_from_data(usr_traj)
    
    file_name = "/home/sscepano/Project7s/D4D/CI/user_stats/OUTPUTfiles/usr_radius_gyr.tsv"
    f = open(file_name, "w")
    
    for usr in rg.keys():
        f.write(str(usr) + '\t' + str(rg[usr]) + '\n')
        

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

# it is much more convenient to read in all user trajectories at once
# and then to calculate the gyration radius here
def calculate_radius_gyration_from_data(usr_traj):
    
    subpref_pos_data = read_in_subpref_pos_file()
    # we save result for each user here
    rg = defaultdict(int)
    
    # this is added after eureka hehe :)
    num_places = 0
    file_name = "/home/sscepano/Project7s/D4D/CI/user_stats/OUTPUTfiles/user_num_places_visited.tsv"
    f = open(file_name, "w")
    
    # loop the users                
    for usr in usr_traj.iterkeys():
            # calculate total number of places visited per user (hehe, I can use this to verify what I calculated before for the number of visited places)
            num_places = 0
            L = 0
            for subpref in usr_traj[usr]:
                if usr_traj[usr][subpref] > 0:
                    L += usr_traj[usr][subpref]
                    num_places += 1
            #print L
            
            f.write(str(usr) + '\t' + str(num_places) + '\n')  
            
            # here we save lon/lat/weight data
            lon = []
            lat = []
            w = []
            # populate the arrays
            for subpref in range(256):
                if usr_traj[usr][subpref] > 0:
                    lon.append(subpref_pos_data[subpref][0])
                    lat.append(subpref_pos_data[subpref][1])
                    w.append(usr_traj[usr][subpref])
            
            # if we found any visited places, then we calculate midpoint for all of them
            # this is what Barabasi calls center of mass of trajectory      
            if len(lon) > 0:        
                center_mass_lon, center_mass_lat = find_mid_point(lon, lat, w)
                
            # we start with zero radius of gyration
            radius_gyr = 0.0
            
            # here we calculate the distances from the midpoint for all the traveled places for the user
            for subpref in range(256):
                if usr_traj[usr][subpref] > 0: 
                    # subtracting tow vectors and then squaring the difference should result in squared distance between them
                    d = find_distance(subpref_pos_data[subpref][0], subpref_pos_data[subpref][1], center_mass_lon, center_mass_lat)
                    ds = d*d
                    # this line I had inversed with the line above and it was not correct calculation
                    # we just here multiply by the number of times we found the user in this place
                    radius_gyr += ds * usr_traj[usr][subpref]
            
            # for users who were not traveling at all (?)        
            if L > 0:    
                radius_gyr = math.sqrt(radius_gyr / L)
                
            # assign this user's radius to output array    
            rg[usr] = radius_gyr  
    
    return rg


# this was a more general function for midpoint I found for lons and lats
def find_mid_point(lon, lat, w):
      
    X = defaultdict(float)
    Y = defaultdict(float)
    Z = defaultdict(float)
    
    for i in range(len(lon)):         
        lat[i] = math.radians(lat[i])
        lon[i] = math.radians(lon[i])
    
        X[i] = math.cos(lat[i])*math.cos(lon[i])
        Y[i] = math.cos(lat[i])*math.sin(lon[i])
        Z[i] = math.sin(lat[i])
        
    #W = float(len(lon))
    W = float(sum(w))
    #print W
    
    x = 0
    y = 0
    z = 0
        
#    x = sum(X) / W
#    print sum(X)
#    y = sum(Y) / W
#    z = sum(Z) / W

    for i in range(len(lon)):
        x += X[i] * w[i]
    
    for i in range(len(lon)):
        y += Y[i] * w[i]
        
    for i in range(len(lon)):
        z += Z[i] * w[i]
        
    x = x / W
    y = y / W
    z = z / W
    
    lon_mid = math.atan2(y,x)
    hyp = math.sqrt(x*x + y*y)
    lat_mid = math.atan2(z, hyp)
    
    lon_mid = math.degrees(lon_mid)
    lat_mid = math.degrees(lat_mid)
                
    return lon_mid, lat_mid 


def find_distance(lon1, lat1, lon2, lat2):
   
    R = 6371
                
    dLat = math.radians(lat2-lat1)
    dLon = math.radians(lon2-lon1)
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)
    a = math.sin(dLat/2) * math.sin(dLat/2) + math.sin(dLon/2) * math.sin(dLon/2) * math.cos(lat1) * math.cos(lat2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    dist = R * c
    
    return dist  