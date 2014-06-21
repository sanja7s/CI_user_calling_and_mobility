'''
Created on Jun 20, 2014

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
        
        avg_usr_traj = defaultdict(float)
    
        usr_traj_SUM = defaultdict(int)
        usr_day_SUM = defaultdict(int)
        usr_total_traj_SUM = defaultdict(int)
        
        for i in range(10):
            
            usr_traj, usr_day, usr_traj_today, usr_total_traj = data[i][0], data[i][1], data[i][2], data[i][3]
            
            for user in usr_traj.keys():
                usr_traj_SUM[user] += usr_traj[user]
                usr_day_SUM[user] += usr_day[user][1]
                usr_total_traj_SUM[user] += usr_total_traj[user]
                    
        for usr in range(500001):
            if usr_day_SUM[usr] > 0:
                avg_usr_traj[usr] = usr_traj_SUM[usr] / float(usr_day_SUM[usr])
                                       
    else:
        print "DID NOTHING in multitasking, as the data seems to be already summed"
    
    return (avg_usr_traj, usr_traj_SUM, usr_day_SUM, usr_total_traj_SUM)