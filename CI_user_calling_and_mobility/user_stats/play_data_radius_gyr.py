'''
Created on Jun 16, 2014

@author: sscepano
'''
from collections import defaultdict

#######################################################################################      
# this one is for calling other functions needed with the data, specific for a set of tasks
#######################################################################################  
def play_data(data1, data2):
    
    data2 = sum_multitasking_output(data1)

    return data2


#######################################################################################      
# do not want to call this one unless the data is an array of 10, i.e., parallel output
### in that case, lets sum it up
#######################################################################################  
def sum_multitasking_output(data):
    
    if len(data) >= 10:
    
        data2 = defaultdict(int)
        
        for i in range(10):
            for user in data[i].keys():
                data2[user] = data2.get(user, defaultdict(int))
                try:
                    for subpref in data[i][user].keys():
                        data2[user][subpref] = data[i][user][subpref]   
                except TypeError:
                    print "TypeError"
                                       
    else:
        print "DID NOTHING in multitasking, as the data seems to be already summed"
    
    return data2