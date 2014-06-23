'''
Created on Jun 23, 2014

@author: sscepano
'''
from collections import defaultdict

#######################################################################################      
# this one is for calling other functions needed with the data
#######################################################################################  
def play_data(data1, data2):
    
    data2 = sum_multitasking_output(data1)
    
# #     print data2[7]['subpref'].pop(-1)
#     print data2[7]['subpref'], sum(data2[7]['subpref'].values())
#     
# #     print data2[11]['subpref'].pop(-1)
#     print data2[11]['subpref'], sum(data2[11]['subpref'].values())


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
                        try:
                            data2[subpref][hr][minut] += data[i][subpref][hr][minut]
                        except TypeError:
                            print "TypeError"
                                       
    else:
        print "DID NOTHING in multitasking, as the data seems to be already summed"
    
    return data2