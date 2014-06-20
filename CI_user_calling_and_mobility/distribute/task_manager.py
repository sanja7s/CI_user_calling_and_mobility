'''
Created on Jun 9, 2014

@author: sscepano
'''
#######################################################################################
### distributes tasks, here all you need is to comment / uncomment lines below
#######################################################################################

#######################################################################################
### here you have tasks for 1: fq and dist places etc., just uncomment
#######################################################################################
# from distribute import user_calling_and_mobility_tasks as u

#######################################################################################
### here you have tasks for 2: radius of gyr, just uncomment, and comment previous, etc.
#######################################################################################
# from distribute import user_radius_of_gyr_tasks as u

#######################################################################################
### here you have tasks for 3: user trajectory, just uncomment, and comment previous, etc.
#######################################################################################
from distribute import user_traj_tasks as u

def distribute_task(data1, data2):
    
    try:
        reload(u)
    except NameError:
        print "NameError"
     
#######################################################################################      
# this part is for reading in the data; comment out after the first step 
### (should work without commenting also)
#######################################################################################   
    if data1 is None:
        print "Read data started"
        data1 = u.read_data()
        print "Read data finished"
        
#######################################################################################      
# this part is for playing with the data, so testing & arranging them as needed
#######################################################################################           
    print "before playing ", len(data1)
    data2 = u.play_data(data1, data2)
    print "after playing ", len(data2)
        
#######################################################################################      
# this part is for saving  the data, after you learned them from playing
#######################################################################################  
    u.save_data(data2)
        
    return data1, data2