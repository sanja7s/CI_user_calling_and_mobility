'''
Created on Jun 9, 2014

@author: sscepano
'''
from distribute import user_calling_and_mobility_tasks as ucm


def distribute_task(data1, data2):
    
    try:
        reload(ucm)
    except NameError:
        print "NameError"
     
#######################################################################################      
# this part is for reading in the data; comment out after the first step 
### (should work without commenting also)
#######################################################################################   
    if data1 is None:
        print "Read data started"
        data1 = ucm.read_data()
        print "Read data finished"
        
#######################################################################################      
# this part is for playing with the data, so testing & arranging them as needed
#######################################################################################           
    print "before playing ", len(data1)
    data2 = ucm.play_data(data1, data2)
    print "after playing ", len(data2)
        
#######################################################################################      
# this part is for saving  the data, after you learned them from playing
#######################################################################################  
#     ucm.save_data(data2)
        
    return data1, data2