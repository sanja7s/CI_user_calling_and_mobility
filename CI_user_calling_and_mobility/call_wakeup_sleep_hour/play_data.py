'''
Created on Aug 12, 2014

@author: sscepano
'''
from collections import defaultdict
import numpy as n

#######################################################################################      
# this one is for calling other functions needed with the data
#######################################################################################  
def play_data(data1, data2):
    
#     data2 = sum_multitasking_output(data1)

#     find_wakeup_hour_Xpct_weekday(data2)
    find_pct_calls_night(data2)

    return data2


#######################################################################################      
# do not want to call this one unless the data is an array of 10, i.e., parallel output
### in that case, lets sum it up
#######################################################################################  
def sum_multitasking_output(data):
    
    if len(data) >= 10:
    
        data2 = defaultdict(int)
        
        for i in range(10):
            for subpref in data[i].keys():
                data2[subpref] = data2.get(subpref, defaultdict(int))
                for hr in data[i][subpref].keys():
                    data2[subpref][hr] = data2[subpref].get(hr, defaultdict(int))
                    for minut in data[i][subpref][hr].keys():
                        data2[subpref][hr][minut] = data2[subpref][hr].get(minut, defaultdict(int))
                        try:
                            data2[subpref][hr][minut]['weekday'] += data[i][subpref][hr][minut]['weekday']
                            data2[subpref][hr][minut]['weekend'] += data[i][subpref][hr][minut]['weekend']
                        except TypeError:
                            print "TypeError"
                                       
    else:
        print "DID NOTHING in multitasking, as the data seems to be already summed. :)"
    
    return data2



#######################################################################################      
# this is some simple hourly analysis to find how many pct we actually seek for
### to be waking up in the morning -- now it looks to me to be even 50%
#######################################################################################  
def find_calls_per_hr_of_weekday(data):
    
    data3 = defaultdict(int)
    
    for subpref in data.keys():
        for hr in data[subpref].keys():
            for minut in data[subpref][hr].keys():
                data3[hr] += data[subpref][hr][minut]['weekday']
    
            
    file_name = "/home/sscepano/Project7s/D4D/CI/call_wakeup_sleep_hour/calls_per_hr_of_weekday.tsv"
    f = open(file_name,"w")
    for hr in data3.keys():
        f.write(str(hr) + '\t' + str(data3[hr]) + '\n')
    
    return data

#######################################################################################      
# this is some simple hourly analysis to find how many pct we actually seek for
### to be waking up in the morning -- now it looks to me to be even 50%
#######################################################################################  
def find_calls_per_hr_of_weekend(data):
    
    data3 = defaultdict(int)
    
    for subpref in data.keys():
        for hr in data[subpref].keys():
            for minut in data[subpref][hr].keys():
                data3[hr] += data[subpref][hr][minut]['weekend']
    
            
    file_name = "/home/sscepano/Project7s/D4D/CI/call_wakeup_sleep_hour/calls_per_hr_of_weekend.tsv"
    f = open(file_name,"w")
    for hr in data3.keys():
        f.write(str(hr) + '\t' + str(data3[hr]) + '\n')
    
    return data

#######################################################################################      
# this one helping with calls per hour per subpref for finding the average
### 
#######################################################################################  
def find_calls_per_subpref_per_hr_of_weekday(data):
    
    data3 = defaultdict(int)
    
    for subpref in data.keys():
        data3[subpref] = data3.get(subpref, defaultdict(int))
        for hr in data[subpref].keys():
            for minut in data[subpref][hr].keys():
                data3[subpref][hr] += data[subpref][hr][minut]['weekday']
    

    
    return data3

#######################################################################################      
# here we find at which our the calling fq for this subpref reaches the above the 
### thresholdX
#######################################################################################  
def find_wakeup_hour_Xpct_weekday(data):
    
    thresholdX = 40
    
    avg_subpref_fq = defaultdict(int)  
    calls_per_subpref_per_hr = find_calls_per_subpref_per_hr_of_weekday(data)
    
    for subpref in data.keys():
        avg_subpref_fq[subpref] = n.mean(list(calls_per_subpref_per_hr[subpref].values()))
        #print list(calls_per_subpref_per_hr[subpref].values()), n.mean(list(calls_per_subpref_per_hr[subpref].values()))
    
            
    file_name = "/home/sscepano/Project7s/D4D/CI/call_wakeup_sleep_hour/avg_calls_per_subpref_weekday.tsv"
    f = open(file_name,"w")
    for subpref in avg_subpref_fq.keys():
        f.write(str(subpref) + '\t' + str(avg_subpref_fq[subpref]) + '\n')
        
#####################################################################################   
#### after finding avg calls per hr per subpref, we now find at which hr they reach 
#### the thresholdX
#####################################################################################       
 
    data3 = defaultdict(int)       
         
    for subpref in calls_per_subpref_per_hr.keys():
        data3[subpref] = data3.get(subpref, defaultdict(int))
        for hr in calls_per_subpref_per_hr[subpref].keys():
            data3[subpref][hr] = float(calls_per_subpref_per_hr[subpref][hr]) / avg_subpref_fq[subpref] * 100
             
             
    subpref_wake_hr = defaultdict(int)
     
    for subpref in data3.keys():
        for hr in [3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,0,1,2]:
            if data3[subpref][hr] >= thresholdX:
                subpref_wake_hr[subpref] = hr
                break
                 
    file_name = "/home/sscepano/Project7s/D4D/CI/call_wakeup_sleep_hour/subpref_wake_" + str(thresholdX) + "pct.tsv"
    f = open(file_name,"w")
    for subpref in subpref_wake_hr.keys():
        f.write(str(subpref) + '\t' + str(subpref_wake_hr[subpref]) + '\n')
    
    return data



#####################################################################################   
#### this is for the calls between 23 and 1
#### 
#####################################################################################       
def find_pct_calls_night(data):
    
    avg_subpref_fq = defaultdict(int)  
    calls_per_subpref_per_hr = find_calls_per_subpref_per_hr_of_weekday(data)
    
    for subpref in data.keys():
        avg_subpref_fq[subpref] = n.mean(list(calls_per_subpref_per_hr[subpref].values()))
        
#####################################################################################   
#### after finding avg calls per hr per subpref, we now find fq 
#### for desired hours
#####################################################################################       
 
    data3 = defaultdict(int)       
         
    for subpref in calls_per_subpref_per_hr.keys():
        data3[subpref] = data3.get(subpref, defaultdict(int))
        for hr in [23,0,1]:
            if avg_subpref_fq[subpref] <> 0:
                data3[subpref][hr] = float(calls_per_subpref_per_hr[subpref][hr]) / avg_subpref_fq[subpref] * 100
            else:
                data3[subpref][hr] = 0
            
    file_name = "/home/sscepano/Project7s/D4D/CI/call_wakeup_sleep_hour/subpref_night_hr_23_0_1_pct_v2.tsv"
    f = open(file_name,"w")
    for subpref in calls_per_subpref_per_hr.keys():
            f.write(str(subpref) + '\t' + str(data3[subpref][23]) + '\t' + str(data3[subpref][0]) + '\t' + str(data3[subpref][1]) + '\t' + str((data3[subpref][23]+data3[subpref][0]+data3[subpref][1])/3) + '\n')
            
            