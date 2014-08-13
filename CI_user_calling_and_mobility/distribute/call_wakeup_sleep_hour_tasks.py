'''
Created on Aug 12, 2014

@author: sscepano
'''
import call_wakeup_sleep_hour.read_in as rd
#import call_wakeup_sleep_hour.save_call_wakeup_sleep_hour as so
import call_wakeup_sleep_hour.map_output as mo
import call_wakeup_sleep_hour.play_data as pd 

#######################################################################################      
# the functions to be called by the distributor -- task manager
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
        reload(mo)
    except Exception as e:
        print e
            
    mo.map_wake_hr(data)

