'''
Created on Jun 16, 2014

@author: sscepano
'''
from collections import defaultdict

#######################################################################################      
# this one is for calling other functions needed with the data
#######################################################################################  
def play_data(data1, data2):
    
#     data2 = sum_multitasking_output(data1)
    
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
            for user in data[i].keys():
                data2[user] = data2.get(user, defaultdict(int))
                data2[user]['subpref'] = data2[user].get('subpref', defaultdict(int))
                try:
                    data2[user]['fq'] += data[i][user]['fq']
                except TypeError:
                    print "TypeError"
                try:
                    for k2 in data[i][user]['subpref'].keys():
                        if data[i][user]['subpref'][k2] == 1:
                            data2[user]['subpref'][k2] = 1    
                except TypeError:
                    print "TypeError"
                                       
    else:
        print "DID NOTHING in multitasking, as the data seems to be already summed"
    
    return data2