'''
Created on Aug 13, 2014

@author: sscepano
'''

###########################################################################################################
### the output saved to a .TSV file  for home and work locations is here reused to plot on a map the commutes
###########################################################################################################

from collections import defaultdict
import dbflib
from matplotlib import cm
from matplotlib.collections import LineCollection
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.basemap import Basemap
from shapelib import ShapeFile

import matplotlib as mpl
import matplotlib.cm as cmx
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


def read_in_subpref_lonlat():
    
    file_name = "/home/sscepano/DATA SET7S/D4D/SUBPREF_POS_LONLAT.TSV"
    f = open(file_name, "r")
    
    subpref_pos = defaultdict(int)
    
    for line in f:
        subpref, lon, lat = line.split('\t')
        subpref = int(subpref)
        lon = float(lon)
        lat = float(lat)
        subpref_pos[subpref] = defaultdict(int)
        subpref_pos[subpref][0] = lon
        subpref_pos[subpref][1] = lat
        
    return subpref_pos



def read_in_subpref_wake_hr(thersholdX):
                  
    file_name = "/home/sscepano/Project7s/D4D/CI/call_wakeup_sleep_hour/subpref_wake_" + str(thersholdX) + "pct.tsv"
    f = open(file_name, "r")
    
    subpref_wake_hr = defaultdict(int)
    
    for line in f:
        subpref, wake_hr = line.split('\t')
        subpref = int(subpref)
        wake_hr = int(wake_hr)
              
        subpref_wake_hr[subpref] = wake_hr
    
    return subpref_wake_hr

def map_wake_hr(thersholdX):

    mpl.rcParams['font.size'] = 4.4
    
    ###########################################################################################
    fig = plt.figure(3)
    #Custom adjust of the subplots
    plt.subplots_adjust(left=0.05,right=0.95,top=0.90,bottom=0.05,wspace=0.15,hspace=0.05)
    ax = plt.subplot(111)
    
    m = Basemap(llcrnrlon=-9, \
                    llcrnrlat=3.8, \
                    urcrnrlon=-1.5, \
                    urcrnrlat = 11, \
                    resolution = 'h', \
                    projection = 'tmerc', \
                    lat_0 = 7.38, \
                    lon_0 = -5.30)
        
    subpref_wake_hr = read_in_subpref_wake_hr(thersholdX)
    # read the shapefile archive
    s = m.readshapefile('/home/sscepano/DATA SET7S/D4D/SubPrefecture/GEOM_SOUS_PREFECTURE', 'subpref')
    
    max7s = 1
    min7s = 10000000
    for subpref in subpref_wake_hr.keys():
        if subpref_wake_hr[subpref] > max7s:
            max7s = subpref_wake_hr[subpref]
        if subpref_wake_hr[subpref] < min7s:
            min7s = subpref_wake_hr[subpref]
            
    max7s = float(max7s)
    print "max", (max7s)
    print "min", (min7s)
    
#     scaled_weight = defaultdict(int)
#     for i in range(256):
#         scaled_weight[i] = defaultdict(int)
#     for subpref in subpref_wake_hr.keys():
#         scaled_weight[subpref] = (subpref_wake_hr[subpref] - min7s) / (max7s - min7s)
    
#     values = range(256)    
#     jet = cm = plt.get_cmap('jet') 
#     cNorm  = colors.Normalize(vmin=0, vmax=values[-1])
#     scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)

    # define custom colormap, white -> nicered, #E6072A = RGB(0.9,0.03,0.16)
    cdict = {'red':  ( (0.0,  1.0,  1.0),
                       (1.0,  0.9,  1.0) ),
             'green':( (0.0,  1.0,  1.0),
                       (1.0,  0.03, 0.0) ),
             'blue': ( (0.0,  1.0,  1.0),
                       (1.0,  0.16, 0.0) ) }
    custom_map = LinearSegmentedColormap('custom_map', cdict, N=33)
    plt.register_cmap(cmap=custom_map)

        
    subpref_coord = read_in_subpref_lonlat()
    
    shp = ShapeFile(r'/home/sscepano/DATA SET7S/D4D/SubPrefecture/GEOM_SOUS_PREFECTURE')
    dbf = dbflib.open(r'/home/sscepano/DATA SET7S/D4D/SubPrefecture/GEOM_SOUS_PREFECTURE')
    
    for npoly in range(shp.info()[0]):
        shpsegs = []
        shpinfo = []
           
        shp_object = shp.read_object(npoly)
        verts = shp_object.vertices()
        rings = len(verts)
        for ring in range(rings):
            lons, lats = zip(*verts[ring])
    #        if max(lons) > 721. or min(lons) < -721. or max(lats) > 91. or min(lats) < -91:
    #            raise ValueError,msg
            x, y = m(lons, lats)
            shpsegs.append(zip(x,y))
            if ring == 0:
                shapedict = dbf.read_record(npoly)
            #print shapedict
            name = shapedict["ID_DEPART"]
            subpref_id = shapedict["ID_SP"]
            print name, subpref_id
            # add information about ring number to dictionary.
            shapedict['RINGNUM'] = ring+1
            shapedict['SHAPENUM'] = npoly+1
            shpinfo.append(shapedict)
        #print subpref_id
        #print name
        lines = LineCollection(shpsegs,antialiaseds=(1,))
        colorVal = custom_map(subpref_wake_hr[subpref_id])
#         colorVal = scaled_weight[subpef]
        lines.set_facecolors(colorVal)
        lines.set_edgecolors('gray')
        lines.set_linewidth(0.1)
        ax.add_collection(lines)  
    
    # data to plot on the map    
    lons = []
    lats = []
    num = []

        
    for subpref in subpref_wake_hr.iterkeys():
        print(subpref)
        if subpref <> 0 and subpref <> -1:
            lons.append(subpref_coord[subpref][0])
            lats.append(subpref_coord[subpref][1])
            num.append(subpref_wake_hr[subpref])
        
    x, y = m(lons, lats)
    m.scatter(x, y, color='white')
    
    for name, xc, yc in zip(num, x, y):
        # draw the pref name in a yellow (shaded) box
            plt.text(xc, yc, name)
            

    
    plt.savefig("/home/sscepano/Project7s/D4D/CI/call_wakeup_sleep_hour/subpref_wake_" + str(thersholdX) + "pct.png",dpi=350)
    
def read_in_subpref_night_hr():
                  
    file_name = "/home/sscepano/Project7s/D4D/CI/call_wakeup_sleep_hour/subpref_night_hr_23_0_1_pct_v2.tsv"
    f = open(file_name, "r")
    
    subpref_wake_hr = defaultdict(int)
    
    for line in f:
        subpref, hr23, hr24, hr1, hrAVG = line.split('\t')
        subpref = int(subpref)
        hr23 = float(hr23)
        hr24 = float(hr24)
        hr1 = float(hr1)
        hrAVG = float(hrAVG)
              
        subpref_wake_hr[subpref] = (hr23, hr24, hr1, hrAVG)
    print hr23, hr24, hr1, hrAVG
    
    return subpref_wake_hr

def map_night_hr(X):
    
    if X == 23:
        X2 = 0
    elif X == 24:
        X2 = 1
    elif X == 1:
        X2 = 2
    else:
        X2 = 3

    mpl.rcParams['font.size'] = 4.4
    
    ###########################################################################################
    fig = plt.figure(3)
    #Custom adjust of the subplots
    plt.subplots_adjust(left=0.05,right=0.95,top=0.90,bottom=0.05,wspace=0.15,hspace=0.05)
    ax = plt.subplot(111)
    
    m = Basemap(llcrnrlon=-9, \
                    llcrnrlat=3.8, \
                    urcrnrlon=-1.5, \
                    urcrnrlat = 11, \
                    resolution = 'h', \
                    projection = 'tmerc', \
                    lat_0 = 7.38, \
                    lon_0 = -5.30)
        
    subpref_night_hr = read_in_subpref_night_hr()
    # read the shapefile archive
    s = m.readshapefile('/home/sscepano/DATA SET7S/D4D/SubPrefecture/GEOM_SOUS_PREFECTURE', 'subpref')
    
    max7s = 1
    min7s = 10000000
    for subpref in subpref_night_hr.keys():
        if subpref_night_hr[subpref][X2] > max7s:
            max7s = subpref_night_hr[subpref][X2]
        if subpref_night_hr[subpref][X2] < min7s and subpref_night_hr[subpref][X2] <> 0:
            min7s = subpref_night_hr[subpref][X2]
             
    max7s = float(max7s)
    print "max", (max7s)
    print "min", (min7s)
    
    scaled_weight = defaultdict(int)
    for i in range(256):
        scaled_weight[i] = defaultdict(int)
    for subpref in subpref_night_hr.keys():
        if subpref_night_hr[subpref][X2] <> 0:
            scaled_weight[subpref] = (subpref_night_hr[subpref][X2] - min7s) / (max7s - min7s)
        else:
            scaled_weight[subpref] = 0
    
#     values = range(256)    
#     jet = cm = plt.get_cmap('jet') 
#     cNorm  = colors.Normalize(vmin=0, vmax=values[-1])
#     scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)

    # define custom colormap, white -> nicered, #E6072A = RGB(0.9,0.03,0.16) #24B79A
    cdict = {'red':  ( (0.0,  1.0,  1.0),
                       (1.0,  0.03,  0.0) ),
             'green':( (0.0,  1.0,  1.0),
                       (1.0,  0.18, 0.0) ),
             'blue': ( (0.0,  1.0,  1.0),
                       (1.0,  0.15, 0.0) ) }
    custom_map = LinearSegmentedColormap('custom_map', cdict, N=44)
    plt.register_cmap(cmap=custom_map)

        
    subpref_coord = read_in_subpref_lonlat()
    
    shp = ShapeFile(r'/home/sscepano/DATA SET7S/D4D/SubPrefecture/GEOM_SOUS_PREFECTURE')
    dbf = dbflib.open(r'/home/sscepano/DATA SET7S/D4D/SubPrefecture/GEOM_SOUS_PREFECTURE')
    
    for npoly in range(shp.info()[0]):
        shpsegs = []
        shpinfo = []
           
        shp_object = shp.read_object(npoly)
        verts = shp_object.vertices()
        rings = len(verts)
        for ring in range(rings):
            lons, lats = zip(*verts[ring])
    #        if max(lons) > 721. or min(lons) < -721. or max(lats) > 91. or min(lats) < -91:
    #            raise ValueError,msg
            x, y = m(lons, lats)
            shpsegs.append(zip(x,y))
            if ring == 0:
                shapedict = dbf.read_record(npoly)
            #print shapedict
            name = shapedict["ID_DEPART"]
            subpref_id = shapedict["ID_SP"]
#             print name, subpref_id
            # add information about ring number to dictionary.
            shapedict['RINGNUM'] = ring+1
            shapedict['SHAPENUM'] = npoly+1
            shpinfo.append(shapedict)
        #print subpref_id
        #print name
        lines = LineCollection(shpsegs,antialiaseds=(1,))
        if int(subpref_night_hr[subpref_id][X2]) <> 0:
            colorVal = custom_map(subpref_night_hr[subpref_id][X2])
        else:
            colorVal = "w"
#         colorVal = scaled_weight[subpef]
        if scaled_weight[subpref_id] <> 0:
            colorVal = custom_map(scaled_weight[subpref_id])
        else:
            colorVal = "w"
        lines.set_facecolors(colorVal)
        lines.set_edgecolors('gray')
        lines.set_linewidth(0.1)
        ax.add_collection(lines)  
    
    # data to plot on the map    
    lons = []
    lats = []
    num = []

        
    for subpref in subpref_night_hr.iterkeys():
#         print(subpref)
        if subpref <> 0 and subpref <> -1:
            lons.append(subpref_coord[subpref][0])
            lats.append(subpref_coord[subpref][1])
            num.append(int(subpref_night_hr[subpref][X2]))
        
    x, y = m(lons, lats)
    m.scatter(x, y, color='white')
    
    for name, xc, yc in zip(num, x, y):
        # draw the pref name in a yellow (shaded) box
            plt.text(xc, yc, name)
            

    plt.savefig("/home/sscepano/Project7s/D4D/CI/call_wakeup_sleep_hour/subpref_night_hr_" + str(X) + "_v2.png",dpi=350)

# map_wake_hr(10)

map_night_hr("24")