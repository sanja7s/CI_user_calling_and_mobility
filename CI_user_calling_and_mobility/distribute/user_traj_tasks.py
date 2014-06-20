'''
Created on Jun 20, 2014

@author: sscepano
'''
import user_stats.read_in_traj as rd
import user_stats.save_traj as so
# import user_stats.map_output as mo
import user_stats.play_data_traj as pd


#######################################################################################      
### the functions to be called by the distributor -- task manager, specific for a set of tasks
#######################################################################################   
def read_data():
    
    try:
        reload(rd)
    except Exception as e:
        print e
    
    print "Read data multiprocesing"
    data = rd.read_in_all_multiprocessing()

    print len(data)
    
    return data

def play_data(data1, data2):
 
    try:
        reload(pd)
    except Exception as e:
        print e
             
    return pd.play_data(data1, data2) 

def save_data(data):

    try:
        reload(so)
    except Exception as e:
        print e
            
    so.save_traj(data) 


    
